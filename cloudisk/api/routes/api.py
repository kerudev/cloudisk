import os

from fastapi import Request
from fastapi.exceptions import HTTPException

from ...fs import CLOUDISK_ROOT
from ..config import app, logger


@app.get("/")
async def get_files(request: Request):
    logger.info("Request on get_files")

    try:
        files = os.listdir(CLOUDISK_ROOT)
    except Exception as e:
        raise HTTPException(500, f"Error when listing {CLOUDISK_ROOT} directory: {e}")

    return files
