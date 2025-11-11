import os
import shutil
from pathlib import Path
from typing import Literal

from . import logger

CLOUDISK_DIR = ".cloudisk"


def ask_remove(storage_path: Path) -> bool:
    while (
        remove := input(
            f"{storage_path} already exists. Do you want to remove it? (y/n)\n> "
        )
    ) not in ("y", "n"):
        logger.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

    return remove == "y"


def remove_file(storage_path: Path) -> Literal[True]:
    storage_path.unlink()
    return True


def remove_dir(storage_path: Path) -> bool:
    # If dir is empty
    if not os.listdir(storage_path):
        storage_path.rmdir()
        return True

    if ask_empty_dir(storage_path) is False:
        return False

    shutil.rmtree(storage_path)

    return True


def ask_empty_dir(storage_path: Path) -> bool:
    while (
        empty_dir := input(
            f"Dir {storage_path} is not empty. Do you want to remove all of its content? (y/n)\n"
        )
    ) not in ("y", "n"):
        logger.error(f"Unexpected answer. Expected 'y' or 'n', got {empty_dir}")

    return empty_dir == "y"


def handle_storage_path_exists(storage_path: Path) -> bool:
    if ask_remove(storage_path) is False:
        return False

    if storage_path.is_file():
        return remove_file(storage_path)

    if storage_path.is_dir():
        return remove_dir(storage_path)

    raise Exception(
        f"{storage_path} already exists and is not a file or a directory. "
        "Please, remove it first."
    )


def init_file_structure() -> bool:
    home_dir = Path.home()
    storage_path = home_dir / CLOUDISK_DIR

    if storage_path.exists():
        # Handle it asking for user consent
        if handle_storage_path_exists(storage_path) is False:
            return False

    storage_path.mkdir()

    return True
