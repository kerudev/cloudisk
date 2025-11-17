import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Query, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, JSONResponse

from cloudisk.fs.utils import is_subpath
from cloudisk.fs.vars import CLOUDISK_ROOT
from cloudisk.infra.logger import get_logger

logger = get_logger("cloudisk.api.files")

files_router = APIRouter(prefix="/files", tags=["files"])


@files_router.get(
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
        None, description=f"File path to be searched from {CLOUDISK_ROOT.as_posix()}"
    ),
):
    logger.info(f"Request on get_files: query_params - {dict(request.query_params)}")

    storage_path = CLOUDISK_ROOT
    if path:
        storage_path = storage_path / path

        if storage_path.is_file():
            return FileResponse(storage_path)

        if not is_subpath(CLOUDISK_ROOT, storage_path):
            files = os.listdir(storage_path)
            return JSONResponse({"files": files})

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

        return FileResponse(storage_path)

    except Exception as e:
        raise HTTPException(
            500, f"Error when listing {storage_path_posix} directory: {e}"
        )
