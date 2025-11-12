from uvicorn import Server

from .config import get_server_config


def run_server():
    server_config = get_server_config()
    server = Server(server_config)
    server.run()
