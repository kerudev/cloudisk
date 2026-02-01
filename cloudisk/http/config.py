from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from cloudisk.db.models.metadata import Metadata
from cloudisk.db.models.user import User
from cloudisk.http.routers import auth, files, root
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
app.include_router(auth.router)
app.include_router(root.router)
app.include_router(files.router)

app.mount("/static", StaticFiles(directory=CLOUDISK_STATIC, html=True), name="static")


# Manage unhandled exceptions to return a JSONResponse
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, e: Exception) -> JSONResponse:
    """Exception handler to catch unhandled exceptions."""
    logger.critical(f"Unhandled exception occurred: {e}")
    return JSONResponse({"message": str(e)}, 500)


@app.exception_handler(User.Error)
async def user_exception_handler(request: Request, e: User.Error) -> None:
    raise HTTPException(400, str(e))


@app.exception_handler(Metadata.Error)
async def metadata_exception_handler(request: Request, e: Metadata.Error) -> None:
    raise HTTPException(400, str(e))
