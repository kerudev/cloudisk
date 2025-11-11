from .config import get_server_config
from uvicorn import Server


def run_server():
    server_config = get_server_config()
    server = Server(server_config)
    server.run()
