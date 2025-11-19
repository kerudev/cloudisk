import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Query, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, JSONResponse

from cloudisk.fs.utils import get_mime_type, is_subpath
from cloudisk.logger import logger
from cloudisk.vars import CLOUDISK_ROOT

files = APIRouter(prefix="/files", tags=["files"])


@files.get(
    "",
    responses={
        200: {"description": "List of files or specific file."},
        400: {"description": "Path is not a directory or a file."},
        403: {"description": "User tried to retrieve files from a non permitted path."},
        404: {"description": "Path does not exist."},
        500: {"description": "Internal server error."},
    },
)
async def get_files(
    request: Request,
    path: Optional[Path] = Query(
        None,
        description=f"File or dir path to be searched from {CLOUDISK_ROOT.as_posix()}",
    ),
):
    logger.info(f"Request on get_files: query_params - {dict(request.query_params)}")

    storage_path = CLOUDISK_ROOT
    if path:
        storage_path = storage_path / path

        if storage_path.is_file():
            return FileResponse(storage_path)

        if not is_subpath(CLOUDISK_ROOT, storage_path):
            raise HTTPException(
                403, f"You are not allowed to retrieve {storage_path.as_posix()}"
            )

    storage_path_posix = storage_path.as_posix()

    if not storage_path.exists():
        raise HTTPException(404, f"{storage_path_posix} path does not exist")

    if not storage_path.is_dir() and not storage_path.is_file():
        raise HTTPException(
            400, f"File {storage_path_posix} is not a directory or a file"
        )

    try:
        if storage_path.is_dir():
            files = os.listdir(storage_path)
            return JSONResponse({"files": files})

        try:
            content_type = get_mime_type(storage_path)
        except Exception as e:
            content_type = None
            logger.warning(f"Could not get mime type for file {storage_path}: {e}")

        if content_type is None:
            # Let Starlette infer file content type
            return FileResponse(storage_path)

        return FileResponse(storage_path, media_type=content_type)

    except Exception as e:
        raise HTTPException(
            500, f"Error when listing {storage_path_posix} directory: {e}"
        )


@files.delete(
    "",
    responses={
        200: {"description": "path deleted correctly."},
        400: {"description": "Path is not a directory or a file."},
        403: {"description": "User tried to delete path from a non permitted one."},
        404: {"description": "Path does not exist."},
        500: {"description": "Internal server error."},
    },
)
async def delete_file(
    request: Request,
    path: Path = Query(
        ...,
        description=f"File or dir path to be deleted from {CLOUDISK_ROOT.as_posix()}",
    ),
):
    logger.info(f"Request on delete_file: query_params - {dict(request.query_params)}")

    storage_path = CLOUDISK_ROOT / path

    storage_path_posix = storage_path.as_posix()

    if not storage_path.exists():
        raise HTTPException(404, f"File at {storage_path_posix} not found")

    if not is_subpath(CLOUDISK_ROOT, storage_path):
        raise HTTPException(403, f"You are not allowed to delete {storage_path_posix}")

    try:
        if storage_path.is_symlink():
            storage_path.unlink()

        elif storage_path.is_dir() or storage_path.is_file():
            os.remove(storage_path)

        else:
            raise HTTPException(
                400,
                f"{storage_path_posix} is not a symlink, "
                "dir or file. It will not be deleted",
            )

    except Exception as e:
        raise HTTPException(500, f"{storage_path_posix} could not be deleted: {e}")

    return JSONResponse({"message": f"{storage_path_posix} deleted correctly"})
