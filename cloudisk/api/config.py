from fastapi import FastAPI, HTTPException, Request

from ..logger import get_logger
from . import API_CONFIG
from .routes import files_router

# Global API logger
logger = get_logger("cloudisk.api")

# Initialize app
app = FastAPI(**API_CONFIG)

# Include routers in app
app.include_router(files_router)


# Manage exceptions, to return a JSON
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, e: Exception):
    logger.critical(f"Unhandled exception occurred: {e}")
    return HTTPException(500, {"detail": "Internal server error"})
