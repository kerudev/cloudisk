from pathlib import Path
from typing import Callable, Concatenate

from cloudisk.logger import get_logger

BoolFunc = Callable[Concatenate[Path, ...], bool]

logger = get_logger("cloudisk.decorators")


def ask_remove_file(func: BoolFunc):
    def wrapper(path: Path, *args, **kwargs) -> bool:
        msg = f"{path} already exists. Do you want to remove it? (y/n)\n> "

        while (remove := input(msg)) not in ("y", "n"):
            logger.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

        if remove == "y":
            return func(path, *args, **kwargs)

        return False

    return wrapper


def ask_empty_dir(func: BoolFunc):
    def wrapper(path: Path, *args, **kwargs) -> bool:
        msg = f"{path} is not empty. Do you want to remove all of its content? (y/n)\n> "

        while (remove := input(msg)) not in ("y", "n"):
            logger.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

        if remove == "y":
            return func(path, *args, **kwargs)

        return False

    return wrapper
