import argparse
from enum import StrEnum, auto
from pathlib import Path
from typing import Annotated, Any, Callable, Literal, Type

from pydantic import BaseModel, Field, field_validator


class CommandName(StrEnum):
    INIT = auto()
    LINK = auto()
    UNLINK = auto()
    RUN = auto()


class Flag(BaseModel):
    short: Annotated[str, Field(freeze=True)]
    long: Annotated[str, Field(freeze=True)]
    type: object
    help: str = ""
    action: Type[argparse.Action] = None
    default: Any = None

    @field_validator("short", mode="before")
    @classmethod
    def validate_short(cls, short: str) -> str:
        if "-" in short:
            raise ValueError("Please provide flags without dashes")

        if len(short) > 1:
            raise ValueError("Short flags must be 1 character long")

        return "-" + short

    @field_validator("long", mode="before")
    @classmethod
    def validate_long(cls, long: str) -> str:
        if "-" in long:
            raise ValueError("Please provide flags without dashes")

        if len(long) < 3:
            raise ValueError("Long flags must be 3 characters long or more")

        return "--" + long

    def model_post_init(self, context: Any):
        if self.type is bool:
            self.action = argparse.BooleanOptionalAction


class RequiredFlag(Flag):
    required: Literal[True] = Field(default=True, frozen=True)

    def __init__(self, **data):  # noqa: D107
        base: Flag

        if not (base := data.pop("base", None)):
            super().__init__(**data)
            return

        data.update(base.model_dump())
        flag = RequiredFlag.model_construct(**data)

        object.__setattr__(self, "__dict__", flag.__dict__)


class OptionalFlag(Flag):
    required: Literal[False] = Field(default=False, frozen=True)

    def __init__(self, **data):  # noqa: D107
        base: Flag

        if not (base := data.pop("base", None)):
            super().__init__(**data)
            return

        data.update(base.model_dump())
        flag = OptionalFlag.model_construct(**data)

        object.__setattr__(self, "__dict__", flag.__dict__)


class Command(BaseModel):
    name: CommandName
    help: str
    action: Callable
    flags: list[Flag] = Field(default_factory=list)
    __parser: argparse.ArgumentParser

    def attach(self, parser: argparse._SubParsersAction):
        self.__parser: argparse.ArgumentParser = parser.add_parser(
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
    __parser: argparse.ArgumentParser

    def model_post_init(self, context: Any):  # noqa: D102
        self.__parser = argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
        )

        subparsers = self.__parser.add_subparsers(dest="command", required=True)

        for command in self.commands:
            command.attach(subparsers)

    def parse(self) -> argparse.Namespace:
        return self.__parser.parse_args()

    def dispatch(self):
        self.run(self.parse())

    def run(self, arguments: argparse.Namespace):
        _args = vars(arguments)
        _command = _args.pop("command")

        for command in self.commands:
            if command.name == _command:
                return command.action(**_args)

        raise ValueError(f"There is no command associated to {_command}")


PATH_FLAGS = Flag(short="p", long="path", type=Path)
