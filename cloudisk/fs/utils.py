import os
import shutil
from pathlib import Path
from urllib.parse import quote

from filetype import guess_mime

from cloudisk.logger import get_logger
from cloudisk.vars import CLOUDISK_ROOT, MB_1

logger = get_logger("cloudisk.fs")


def get_mime_type(path: Path) -> str | None:
    """Get mime type of the given file."""
    if not path.is_file():
        return None

    return guess_mime(path)


def is_subpath(child_path: Path, parent_path: Path = CLOUDISK_ROOT) -> bool:
    """Check if child path is subpath of parent_path."""
    parent_path = path_resolve(parent_path)
    child_path = path_resolve(child_path)

    if child_path == parent_path:
        return False

    return parent_path in child_path.parents


def is_parent_path(child_path: Path, parent_path: Path = CLOUDISK_ROOT) -> bool:
    """Check if child path is superpath of parent_path."""
    parent_path = path_resolve(parent_path)
    child_path = path_resolve(child_path)

    if child_path == parent_path:
        return False

    return parent_path not in child_path.parents


def path_resolve(path: Path) -> Path:
    if path.is_symlink():
        return path

    for parent in path.parents:
        if parent.is_symlink():
            return path

    return path.resolve()


def ask_remove_file(path: Path) -> bool:
    msg = f"{path} already exists. Do you want to remove it? (y/n)\n> "

    while (remove := input(msg)) not in ("y", "n"):
        logger.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

    if remove == "n":
        return False

    path.unlink()

    return True


def ask_remove_dir(path: Path) -> bool:
    msg = f"{path} is not empty. Do you want to remove all of its content? (y/n)\n> "

    while (remove := input(msg)) not in ("y", "n"):
        logger.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

    if remove == "n":
        return False

    # If dir is empty
    if not os.listdir(path):
        path.rmdir()
        return True

    shutil.rmtree(path)

    return True


def ask_remove_path(path: Path) -> bool:
    if path.is_file():
        return ask_remove_file(path)

    if path.is_dir():
        return ask_remove_dir(path)

    raise Exception(
        f"{path} already exists and is not a file or a directory. "
        "Please, remove it first."
    )


def attachment_content_disposition(file_name: str):
    if (header_filename := quote(file_name)) != file_name:
        return f"attachment; filename*=utf-8''{header_filename}"
    else:
        return f'attachment; filename="{file_name}"'


def iter_file_chunks(path: Path, chunk_size: int = MB_1):
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk
