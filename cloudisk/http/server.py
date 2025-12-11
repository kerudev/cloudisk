from uvicorn import Config, Server

from cloudisk.http.config import app


def get_server_config(host: str, port: int) -> Config:
    """
    Get configuration for uvicorn server.

    Parameters
    ----------
    host : str
        Host address to run server in.
    port : int
        Port to run server in.

    Returns
    -------
    uvicorn.Config
        Uvicorn server configuration.
    """
    return Config(app=app, host=host, port=port)


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    """
    Run server with the given parameters.

    Parameters
    ----------
    host : str, optional
        Host address to run server in. By default, 0.0.0.0.
    port : int
        Port to run server in. By default, 8000.
    """
    server_config = get_server_config(host=host, port=port)
    server = Server(server_config)
    server.run()
