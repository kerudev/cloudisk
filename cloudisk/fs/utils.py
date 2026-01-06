import os
import shutil
from pathlib import Path
from typing import Iterator
from urllib.parse import quote

from filetype import guess_mime

from cloudisk.logger import get_logger
from cloudisk.vars import CLOUDISK_ROOT, MB_1

logger = get_logger("cloudisk.fs")


def get_mime_type(path: Path) -> str | None:
    """
    Get mime type of the given file.

    Parameters
    ----------
    path : Path
        File path to get mime type from.

    Returns
    -------
    str | None
        Mime type of file. None if path is not a file or mime type could not be gotten.
    """
    if not path.is_file():
        return None

    return guess_mime(path)


def is_subpath(child_path: Path, parent_path: Path = None) -> bool:
    """
    Check if child path is subpath of parent_path.

    Parameters
    ----------
    child_path : Path
        Child path to check if it is a subpath.
    parent_path : Path, optional
        Parent path to check if child_path is subpath of it.

    Returns
    -------
    bool
        True if child path is subpath of parent path.
        False otherwise or if both paths are the same.
    """
    parent_path = path_resolve(parent_path or CLOUDISK_ROOT)
    child_path = path_resolve(child_path)

    if child_path == parent_path:
        return False

    return parent_path in child_path.parents


def is_parent_path(child_path: Path, parent_path: Path = None) -> bool:
    """
    Check if child path is superpath of parent_path.

    Parameters
    ----------
    child_path : Path
        Child path to check if parent_path is superpath of it.
    parent_path : Path, optional
        Parent path to check if it is a superpath.

    Returns
    -------
    bool
        True if parent path is a superpath of child path.
        False otherwise or if both paths are the same.
    """
    parent_path = path_resolve(parent_path or CLOUDISK_ROOT)
    child_path = path_resolve(child_path)

    if child_path == parent_path:
        return False

    return parent_path not in child_path.parents


def path_resolve(path: Path) -> Path:
    """
    Get absolute path and normalize it.
    If path or any of its parents are symlinks, same path will be returned.

    Parameters
    ----------
    path : Path
        Path to be resolved.

    Returns
    -------
    pathlib.Path
        Resolved path or same one if path or any of its parents are symlinks.
    """
    if path.is_symlink():
        return path

    for parent in path.parents:
        if parent.is_symlink():
            return path

    return path.resolve()


def ask_remove_file(path: Path) -> bool:
    """
    Ask for permission to remove a file and remove it if user agrees.

    Parameters
    ----------
    path : Path
        File path to be deleted.

    Returns
    -------
    bool
        True if deleted. False otherwise.
    """
    msg = f"{path} already exists. Do you want to remove it? (y/n)\n> "

    while (remove := input(msg)) not in ("y", "n"):
        logger.error(f"Unexpected answer. Expected 'y' or 'n', got {remove}")

    if remove == "n":
        return False

    path.unlink()

    return True


def ask_remove_dir(path: Path) -> bool:
    """
    Ask for permission to remove a dir and remove it if user agrees.

    Parameters
    ----------
    path : Path
        Directory path to be deleted.

    Returns
    -------
    bool
        True if deleted. False otherwise.
    """
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
    """
    Ask to remove a path depending on its type.

    Parameters
    ----------
    path : Path
        File or directory path to be removed.

    Returns
    -------
    bool
        True if deleted. False otherwise.

    Raises
    ------
    Exception
        If path is not a file or a directory.
    """
    if path.is_file():
        return ask_remove_file(path)

    if path.is_dir():
        return ask_remove_dir(path)

    raise Exception(
        f"{path} already exists and is not a file or a directory. "
        "Please, remove it first."
    )


def attachment_content_disposition(file_name: str) -> str:
    """
    Return attachment content disposition depending on filename.

    Parameters
    ----------
    file_name : str
        Filename to get attachment content disposition.

    Returns
    -------
    str
        Attachment content disposition depending on whether it needs to be quoted or not.
    """
    if (header_filename := quote(file_name)) != file_name:
        return f"attachment; filename*=utf-8''{header_filename}"

    return f'attachment; filename="{file_name}"'


def iter_file_chunks(path: Path, chunk_size: int = MB_1) -> Iterator[bytes]:
    """
    Iterate over file content chunks.

    Parameters
    ----------
    path : Path
        File path to get content from.
    chunk_size : int, optional
        Content bytes size to be chunked. By default MB_1

    Yields
    ------
    Iterator[bytes]
        Chunked content bytes.
    """
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk
