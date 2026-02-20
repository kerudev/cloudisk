import os

from fastapi.testclient import TestClient

from cloudisk.http.config import app
from cloudisk.http.vars import CLOUDISK_STATIC

client = TestClient(app)


def test_root():
    response = client.get("/")

    with open(
        CLOUDISK_STATIC / "index.html",
        encoding="utf-8",
        newline=os.linesep,
    ) as f:
        expected = f.read()

    assert response.status_code == 200
    assert response.text == expected
