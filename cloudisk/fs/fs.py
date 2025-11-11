import os
import shutil
from pathlib import Path
from typing import Literal

from .decorators import ask_empty_dir, ask_remove_file

CLOUDISK_DIR = ".cloudisk"


@ask_remove_file
def remove_file(path: Path) -> Literal[True]:
    path.unlink()
    return True


@ask_empty_dir
def remove_dir(path: Path) -> bool:
    # If dir is empty
    if not os.listdir(path):
        path.rmdir()
        return True

    shutil.rmtree(path)

    return True


def check_path(path: Path) -> bool:
    if path.is_file():
        return remove_file(path)

    if path.is_dir():
        return remove_dir(path)

    raise Exception(
        f"{path} already exists and is not a file or a directory. "
        "Please, remove it first."
    )


def init_file_structure(path: Path) -> bool:
    # Handle it asking for user consent
    if path.exists() and not check_path(path) is False:
        return False

    path.mkdir()

    return True
