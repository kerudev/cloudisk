from uvicorn import Config

from ..api.config import app


def get_server_config():
    return Config(app=app, host="0.0.0.0", port=8000)
