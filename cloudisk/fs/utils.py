import os
import shutil
from pathlib import Path
from typing import Literal

from filetype import guess_mime

from cloudisk.vars import CLOUDISK_ROOT

from .decorators import ask_empty_dir, ask_remove_file


def get_mime_type(path: Path) -> str | None:
    """Get mime type of the given file."""
    if not path.is_file():
        return None

    return guess_mime(path)


def is_subpath(child_path: Path, parent_path: Path = CLOUDISK_ROOT) -> bool:
    """Check if child path is subpath of parent_path."""
    # Normalize child parents paths
    return parent_path.resolve() in (parent.resolve() for parent in child_path.parents)


def is_parent_path(child_path: Path, parent_path: Path = CLOUDISK_ROOT) -> bool:
    """Check if child path is superpath of parent_path."""
    # Normalize child parents paths
    return not is_subpath(child_path, parent_path)


@ask_remove_file
def remove_file(path: Path) -> Literal[True]:
    path.unlink()
    # TODO. Remove metadata
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
