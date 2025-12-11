from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from cloudisk.http.routers import files, root
from cloudisk.logger import get_logger
from cloudisk.vars import CLOUDISK_STATIC

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
app.include_router(root)
app.include_router(files)

app.mount("/static", StaticFiles(directory=CLOUDISK_STATIC, html=True), name="static")


# Manage unhandled exceptions to return a JSONResponse
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, e: Exception) -> JSONResponse:
    """Exception handler to catch unhandled exceptions."""
    logger.critical(f"Unhandled exception occurred: {e}")
    return JSONResponse({"message": "Internal server error"}, 500)
