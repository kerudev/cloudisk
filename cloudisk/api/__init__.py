from .routes import files_router


API_CONFIG = {
    "title": "cloudisk_api",
    "description": "API to manage cloudisk files",
    "version": "0.1.0",
    "openapi_tags": [
        {"name": "files", "description": "Operations related to files management."}
    ],
}


__all__ = [
    "API_CONFIG",
    "files_router",
]
