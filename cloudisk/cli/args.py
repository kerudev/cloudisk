from argparse import ArgumentParser, Namespace, _SubParsersAction
from enum import StrEnum, auto
from pathlib import Path
from typing import Annotated, Any, Callable, Literal

from pydantic import AfterValidator, BaseModel, Field

from cloudisk.logger import get_logger

logger = get_logger("cloudisk.args")


class CommandName(StrEnum):
    INIT = auto()
    LINK = auto()
    UNLINK = auto()
    RUN = auto()


class Flag(BaseModel):
    short: str = Annotated[Field(frozen=True), AfterValidator("_validate_short")]
    long: str = Annotated[Field(frozen=True), AfterValidator("_validate_long")]
    type: object
    help: str = ""
    required: bool = True

    @classmethod
    def _validate_short(cls, short: str) -> str:
        if short.replace("-", "") != short:
            raise ValueError("Please provide flags without dashes")

        if len(short) > 1:
            raise ValueError("Short flags must be 1 character long")

        return short

    @classmethod
    def _validate_long(cls, long: str) -> str:
        if long.replace("-", "") != long:
            raise ValueError("Please provide flags without dashes")

        if len(long) < 3:
            raise ValueError("Long flags must be 3 characters long or more")

        return long


class RequiredFlag(Flag):
    required: Literal[True] = Field(default=True, frozen=True)

    def __init__(self, **data):  # noqa: D107
        base: Flag = data.pop("base", None)

        if base:
            data.update(base.model_dump())

        super().__init__(**data)


class OptionalFlag(Flag):
    required: Literal[False] = Field(default=False, frozen=True)


class Command(BaseModel):
    name: CommandName
    help: str
    action: Callable
    flags: list[Flag] = Field(default_factory=list)
    __parser: ArgumentParser

    def attach(self, parser: _SubParsersAction):
        self.__parser: ArgumentParser = parser.add_parser(
            self.name.value,
            help=self.help,
        )

        if not self.flags:
            return

        for flag in self.flags:
            model = flag.model_dump()
            flags = (model.pop("short"), model.pop("long"))

            self.__parser.add_argument(*flags, **model)

    def run(self, *args, **kwargs):
        self.action(*args, **kwargs)


class Parser(BaseModel):
    name: str
    description: str
    commands: list[Command]
    __parser: ArgumentParser

    def model_post_init(self, context: Any):  # noqa: D102
        self.__parser = ArgumentParser(
            prog=self.name,
            description=self.description,
        )

        subparsers = self.__parser.add_subparsers(dest="command", required=True)

        for command in self.commands:
            command.attach(subparsers)

    def parse(self) -> Namespace:
        return self.__parser.parse_args()

    def dispatch(self):
        self.run(self.parse())

    def run(self, arguments: Namespace):
        _args = vars(arguments)
        _command = _args.pop("command")

        for command in self.commands:
            if command.name == _command:
                return command.action(**_args)

        raise ValueError(f"There is no command associated to {_command}")


PATH_FLAGS = Flag(short="-p", long="--path", type=Path)
