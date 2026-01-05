from unittest.mock import patch

from uvicorn import Config, Server

from cloudisk.http import server
from cloudisk.http.config import app


def test_run_default():
    with (
        patch.object(server, "Config", wraps=Config) as mock_config,
        patch.object(server, "Server", spec=Server) as mock_server,
    ):
        server.run()

    args = mock_config.call_args[1]

    assert args["app"] == app
    assert args["host"] == "0.0.0.0"
    assert args["port"] == 8000

    mock_server.return_value.run.assert_called_once()


def test_run_custom():
    with (
        patch.object(server, "Config", wraps=Config) as mock_config,
        patch.object(server, "Server", spec=Server) as mock_server,
    ):
        server.run(app=app, host="127.0.0.1", port=8080)

    args = mock_config.call_args[1]

    assert args["app"] == app
    assert args["host"] == "127.0.0.1"
    assert args["port"] == 8080

    mock_server.return_value.run.assert_called_once()
