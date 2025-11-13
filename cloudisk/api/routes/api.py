import os

from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse

from ...fs import CLOUDISK_ROOT
from ..config import app, logger


@app.get("/")
async def root():
    logger.info("Request on root")
    return FileResponse("./cloudisk/static/index.html")


@app.get("/files")
async def files():
    logger.info("Request on files")

    try:
        return os.listdir(CLOUDISK_ROOT)
    except Exception as e:
        raise HTTPException(500, f"Error when listing {CLOUDISK_ROOT} directory: {e}")
