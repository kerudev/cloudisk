from pathlib import Path
from tomllib import load

from fastapi import FastAPI, HTTPException, Request

from . import get_logger
from .routes import files_router

CONFIG_FILE = Path(__file__).parent / "config.toml"


def get_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "rb") as f:
        return load(f)


api_config = get_config()


logger = get_logger("cloudisk.api")


app = FastAPI(
    title=api_config.get("name", "cloudisk_api"),
    description=api_config.get("description", "API to manage cloudisk files"),
    version=api_config.get("version", "0.1.0"),
    openapi_tags=api_config.get("TAGS", []),
)


app.include_router(files_router)


# Manage exceptions, to return a JSON
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, e: Exception):
    logger.critical(f"Unhandled exception occurred: {e}")
    return HTTPException(500, {"detail": "Internal server error"})
