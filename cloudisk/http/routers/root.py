from fastapi import APIRouter
from fastapi.responses import FileResponse

from cloudisk.logger import logger
from cloudisk.vars import CLOUDISK_STATIC

router = APIRouter(prefix="", tags=["root"])


@router.get("/")
async def index():
    """Index route."""
    logger.info("Request on index")
    return FileResponse(CLOUDISK_STATIC / "index.html")
