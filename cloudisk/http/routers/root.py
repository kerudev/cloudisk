from fastapi import APIRouter
from fastapi.responses import FileResponse

from cloudisk.http.vars import CLOUDISK_STATIC

router = APIRouter(prefix="", tags=["root"])


@router.get("/")
async def index():
    """Index route."""
    return FileResponse(CLOUDISK_STATIC / "index.html")
