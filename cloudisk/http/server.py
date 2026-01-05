from typing import Optional

from fastapi import FastAPI
from uvicorn import Config, Server


def run(host: str = "0.0.0.0", port: int = 8000, app: Optional[FastAPI] = None) -> None:
    """
    Run server with the given parameters.

    Parameters
    ----------
    host : str, optional
        Host address to run server in. By default, 0.0.0.0.
    port : int
        Port to run server in. By default, 8000.
    app : Optional[FastAPI] = None
        A FastAPI instance.
    """
    if not app:
        from cloudisk.http.config import app as fastapi

        app = fastapi

    config = Config(app=app, host=host, port=port)
    server = Server(config)
    server.run()
