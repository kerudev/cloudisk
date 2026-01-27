from unittest.mock import patch

from cloudisk.http import server


def test_run_default():
    with patch.object(server, "uvicorn") as mock_uvicorn:
        server.run()

    args = mock_uvicorn.run.call_args[1]

    assert args["app"] == "cloudisk.http.config:app"
    assert args["host"] == "0.0.0.0"
    assert args["port"] == 8000

    mock_uvicorn.run.assert_called_once()


def test_run_custom():
    with patch.object(server, "uvicorn") as mock_uvicorn:
        server.run(host="127.0.0.1", port=8080)

    args = mock_uvicorn.run.call_args[1]

    assert args["app"] == "cloudisk.http.config:app"
    assert args["host"] == "127.0.0.1"
    assert args["port"] == 8080

    mock_uvicorn.run.assert_called_once()
