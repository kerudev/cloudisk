from fastapi import FastAPI, HTTPException, Request

from ..config import config
from . import get_logger

TAGS = [{"name": "files", "description": "Operations related to files management."}]


logger = get_logger("cloudisk.api")


app = FastAPI(
    title="cloudisk_API",
    description="API to manage cloudisk files",
    version=config.get("version", "0.1.0"),
    openapi_tags=TAGS,
)


# Manage exceptions, to return a JSON
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, e: Exception):
    logger.critical(f"Unhandled exception occurred: {e}")
    return HTTPException(500, {"detail": "Internal server error"})
