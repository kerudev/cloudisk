from fastapi.testclient import TestClient

from cloudisk.http.config import app
from cloudisk.vars import CLOUDISK_STATIC

client = TestClient(app)


def test_root():
    response = client.get("/")

    with open(CLOUDISK_STATIC / "index.html", "r", encoding="utf-8") as f:
        expected = f.read()

    assert response.status_code == 200
    assert response.text == expected
