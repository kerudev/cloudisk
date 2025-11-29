from pathlib import Path

from fastapi import HTTPException, Query

from cloudisk.fs.utils import is_parent_path, path_resolve
from cloudisk.vars import CLOUDISK_ROOT, METADATA_PATH

EXCLUDED_PATHS = [METADATA_PATH]


async def validate_path(path: Path = Query("")):
    """Prevents tree traversal (going backwards from the root directory)."""
    storage_path = path_resolve(CLOUDISK_ROOT / path)

    if storage_path == CLOUDISK_ROOT:
        return path

    if is_parent_path(storage_path) or storage_path in EXCLUDED_PATHS:
        raise HTTPException(
            403, f"You are not allowed to retrieve {storage_path.as_posix()}"
        )

    return path
