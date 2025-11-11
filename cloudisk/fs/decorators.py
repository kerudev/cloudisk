from pathlib import Path
from typing import Callable

from cloudisk import logger


def ask_remove_file(func: Callable):
    def wrapper(path: Path, *args, **kwargs):
        msg = f"{path} already exists. Do you want to remove it? (y/n)\n> "

        while (remove := input(msg)) not in ("y", "n"):
            logger.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

        if remove == "y":
            return func(path, *args, **kwargs)

    return wrapper


def ask_empty_dir(func: Callable) -> bool:
    def wrapper(path: Path, *args, **kwargs):
        msg = f"{path} is not empty. Do you want to remove all of its content? (y/n)\n> "

        while (remove := input(msg)) not in ("y", "n"):
            logger.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

        if remove == "y":
            return func(path, *args, **kwargs)

    return wrapper
