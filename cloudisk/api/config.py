from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles

from ..fs import CLOUDISK_STATIC
from ..logger import get_logger
from .routes import files_router, root_router

API_CONFIG = {
    "title": "cloudisk_api",
    "description": "API to manage cloudisk files",
    "version": "0.1.0",
    "openapi_tags": [
        {"name": "files", "description": "Operations related to files management."}
    ],
}

# Global API logger
logger = get_logger("cloudisk.api")

# Initialize app
app = FastAPI(**API_CONFIG)

# Include routers in app
app.include_router(root_router)
app.include_router(files_router)

app.mount("/static", StaticFiles(directory=CLOUDISK_STATIC, html=True), name="static")


# Manage exceptions, to return a JSON
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, e: Exception):
    logger.critical(f"Unhandled exception occurred: {e}")
    return HTTPException(500, {"detail": "Internal server error"})
