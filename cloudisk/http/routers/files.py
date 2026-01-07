import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from cloudisk.fs.metadata import MetadataManager
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

router = APIRouter(prefix="/files", tags=["files"])


async def _list_files(path: Path) -> JSONResponse:
    """
    List files in the given path. This is not expected to be called directly,
    but through `get_files`.

    Parameters
    ----------
    path : Path
        The directory to list files from. This is expected to be a directory,
        as it doesn't make sense to list files inside a file. If `path` is a
        file, an exception will be raised.

    Returns
    -------
    JSONResponse
        JSONResponse containing files list.

    Raises
    ------
    HTTPException - 400
        If the given path is not a directory.
    HTTPException - 404
        If the given path does not exist.
    HTTPException - 500
        If an error occurs listing files in the directory.
    """
    if not path.exists():
        raise HTTPException(404, f"{path.as_posix()} path does not exist")

    try:
        files = sorted(
            path.iterdir(),
            key=lambda x: (not x.is_dir(), x.name.casefold()),
        )

        if available_paths := MetadataManager().available_paths:
            files = list(filter(lambda file: str(file) in available_paths, files))

        files = list(filter(lambda file: file.name not in EXCLUDED_FILES, files))
        files = [file.name for file in files]

    except Exception as e:
        raise HTTPException(500, f"Error when listing {path.as_posix()} directory: {e}")

    return JSONResponse({"files": files, "isRoot": path == CLOUDISK_ROOT})


async def _download_files(path: Path) -> FileResponse | StreamingResponse:
    """
    Download the given file.

    Parameters
    ----------
    path : Path
        File path to be downloaded.

    Returns
    -------
    FileResponse | StreamingResponse
        Downloaded file bytes.
    """
    MetadataManager().update_downloads(path)

    content_type = get_mime_type(path)

    if path.stat().st_size <= MB_100:
        return FileResponse(path, filename=path.name, media_type=content_type)

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


@router.get(
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
    """
    Get files list if path is directory. Else, download file.

    Parameters
    ----------
    request : fastapi.Request
        FastAPI request object.
    path : Path
        Path that is being accessed.
    """
    logger.info(f"Request on get_files: query_params - {dict(request.query_params)}")

    storage_path = path_resolve(CLOUDISK_ROOT / path)

    endpoint = _download_files if storage_path.is_file() else _list_files
    response = await endpoint(storage_path)

    return response


@router.post(
    "",
    responses={
        201: {"description": "List of files or specific file."},
        403: {"description": "User tried to create a file in a non permitted path."},
    },
)
async def upload_file(files: list[UploadFile] = File(...)):
    """
    Upload a file or list of files to the cloudisk root directory.

    Parameters
    ----------
    files : list[UploadFile]
        List of files that are being uploaded.
    """
    for file in files:
        filename = Path(file.filename)
        path = CLOUDISK_ROOT / filename

        if not is_subpath(path):
            raise HTTPException(403, f"You are not allowed to create {path.as_posix()}")

        i = 1
        while path.exists():
            path = path.with_stem(f"{filename.stem}_{i}")
            i += 1

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            MetadataManager().create(path)
        except Exception as e:
            # TODO return the names of the files that failed to upload
            logger.error(f"There was an error while uploading {path}: {e}")
            os.remove(path)

    return await _list_files(CLOUDISK_ROOT)


@router.delete(
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
    """
    Delete a file or directory from the cloudisk root directory.

    Parameters
    ----------
    request : fastapi.Request
        FastAPI request object.
    path : Path
        Path to the file or directory to be deleted.

    Raises
    ------
    HTTPException - 400
        If the given path is not a directory or a file.
    HTTPException - 403
        If the given path is not a permitted path.
    HTTPException - 404
        If the given path does not exist.
    HTTPException - 500
        If an error occurs deleting the file or directory.
    """
    logger.info(f"Request on delete_file: query_params - {dict(request.query_params)}")

    storage_path = CLOUDISK_ROOT / path

    if not is_subpath(storage_path):
        raise HTTPException(
            403, f"You are not allowed to delete {storage_path.as_posix()}"
        )

    if not storage_path.exists():
        raise HTTPException(404, f"File at {storage_path.as_posix()} not found")

    try:
        MetadataManager().remove(storage_path)
    except Exception as e:
        raise HTTPException(500, f"{storage_path.as_posix()} could not be deleted: {e}")

    return JSONResponse({"message": f"{storage_path.as_posix()} deleted correctly"})
