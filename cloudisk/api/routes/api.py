from fastapi import APIRouter
from fastapi.responses import FileResponse

from ...fs import CLOUDISK_STATIC
from ...logger import get_logger

logger = get_logger("cloudisk.api")

root_router = APIRouter(prefix="", tags=["root"])


@root_router.get("/")
async def root():
    logger.info("Request on root")
    return FileResponse(CLOUDISK_STATIC / "index.html")
