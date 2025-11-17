from uvicorn import Config, Server

from cloudisk.http.config import app


def get_server_config():
    return Config(app=app, host="0.0.0.0", port=8000)


def run():
    server_config = get_server_config()
    server = Server(server_config)
    server.run()
