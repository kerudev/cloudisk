import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from cloudisk.fs.utils import (
    attachment_content_disposition,
    get_mime_type,
    is_subpath,
    iter_file_chunks,
    path_resolve,
)
from cloudisk.http.dependencies import validate_path
from cloudisk.logger import logger
from cloudisk.vars import CLOUDISK_ROOT, MB_100, METADATA_FILE

EXCLUDED_FILES = [METADATA_FILE]

files = APIRouter(prefix="/files", tags=["files"])


async def _list_files(path: Path):
    path_posix = path.as_posix()

    if not path.exists():
        raise HTTPException(404, f"{path_posix} path does not exist")

    if not path.is_dir():
        raise HTTPException(400, f"File {path_posix} is not a directory")

    try:
        file_list = sorted(
            path.iterdir(),
            key=lambda x: (not x.is_dir(), x.name.casefold()),
        )
        file_list = [file.name for file in file_list if file.name not in EXCLUDED_FILES]

    except Exception as e:
        raise HTTPException(500, f"Error when listing {path_posix} directory: {e}")

    return JSONResponse({"files": file_list})


async def _download_files(path: Path):
    try:
        content_type = get_mime_type(path)
    except Exception as e:
        logger.warning(f"Could not get mime type for file {path}: {e}")
        return FileResponse(path, filename=path.name)

    if path.stat().st_size > MB_100:
        content_disposition = attachment_content_disposition(path.name)

        headers = {
            "content-length": str(path.stat().st_size),
            "content-disposition": content_disposition,
        }

        return StreamingResponse(
            iter_file_chunks(path),
            206,
            headers=headers,
            media_type=content_type,
        )

    return FileResponse(path, filename=path.name, media_type=content_type)


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
async def get_files(request: Request, path: Path = Depends(validate_path)):
    logger.info(f"Request on get_files: query_params - {dict(request.query_params)}")

    storage_path = path_resolve(CLOUDISK_ROOT / path)

    endpoint = _download_files if storage_path.is_file() else _list_files
    response = await endpoint(storage_path)

    return response


@files.post(
    "",
    responses={
        201: {"description": "List of files or specific file."},
        403: {"description": "User tried to create a file in a non permitted path."},
    },
)
async def upload_file(files: list[UploadFile] = File(...)):
    for file in files:
        filename = Path(file.filename)
        # file_type = file.content_type

        path = CLOUDISK_ROOT / filename

        if not is_subpath(path):
            raise HTTPException(403, f"You are not allowed to create {path.as_posix()}")

        i = 1
        while path.exists():
            path = path.with_stem(f"{filename.stem}_{i}")
            i += 1

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return _list_files(path)


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

    if not is_subpath(storage_path):
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
