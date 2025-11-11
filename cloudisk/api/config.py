from fastapi import APIRouter, FastAPI

from ..config import config

TAGS = [{"files": "Operations related to files management."}]


files = APIRouter(prefix="/files", tags=["files"])

app = FastAPI(
    title="cloudisk_API",
    description="API to manage cloudisk files",
    version=config.get("version", "0.1.0"),
    openapi_tags=TAGS,
)

app.include_router(files)
