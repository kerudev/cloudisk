from pathlib import Path

from fastapi import HTTPException, Query

from cloudisk.fs.utils import is_parent_path, path_resolve
from cloudisk.vars import CLOUDISK_DB_PATH, CLOUDISK_ROOT

EXCLUDED_PATHS = [CLOUDISK_DB_PATH]


async def validate_path(path: Path = Query("")) -> Path:
    """
    Prevents tree traversal (going backwards from the root directory).

    Parameters
    ----------
    path : Path
        Path to check if is backwards from the root directory.

    Returns
    -------
    pathlib.Path
        Received path parameter.

    Raises
    ------
    HTTPException
        If given path is backwards from the root directory or in excluded paths.
    """
    storage_path = path_resolve(CLOUDISK_ROOT / path)

    if storage_path == CLOUDISK_ROOT:
        return path

    if is_parent_path(storage_path) or storage_path in EXCLUDED_PATHS:
        raise HTTPException(
            403, f"You are not allowed to retrieve {storage_path.as_posix()}"
        )

    return path
