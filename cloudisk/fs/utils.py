import os
import shutil
from pathlib import Path
from typing import Literal

from .decorators import ask_empty_dir, ask_remove_file


@ask_remove_file
def remove_file(path: Path) -> Literal[True]:
    path.unlink()
    return True


@ask_empty_dir
def remove_dir(path: Path) -> Literal[True]:
    # If dir is empty
    if not os.listdir(path):
        path.rmdir()
        return True

    shutil.rmtree(path)

    return True


def remove_path(path: Path) -> bool:
    if path.is_file():
        return remove_file(path)

    if path.is_dir():
        return remove_dir(path)

    raise Exception(
        f"{path} already exists and is not a file or a directory. "
        "Please, remove it first."
    )
