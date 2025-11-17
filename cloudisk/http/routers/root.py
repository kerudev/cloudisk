from fastapi import APIRouter
from fastapi.responses import FileResponse

from cloudisk.logger import logger
from cloudisk.vars import CLOUDISK_STATIC

root = APIRouter(prefix="", tags=["root"])


@root.get("/")
async def index():
    logger.info("Request on index")
    return FileResponse(CLOUDISK_STATIC / "index.html")
