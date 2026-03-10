import pytest
from fastapi.testclient import TestClient

from cloudisk.db.models import User
from cloudisk.http.config import app
from tests.conftest import TEST_MAIL, TEST_PASS, TEST_USER

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_send_verify_email(monkeypatch):
    monkeypatch.setattr(
        "cloudisk.db.models.user.User._send_verify_email", lambda _, __: ...
    )


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "username": TEST_USER,
            "email": TEST_MAIL,
            "password": TEST_PASS,
        },
    )

    user = response.json()

    expected_user = {
        "id": 1,
        "space_id": 999,
        "username": TEST_USER,
        "email": TEST_MAIL,
        "password": TEST_PASS,
        "last_login": None,
        "is_verified": False,
    }

    assert user == expected_user


def test_verify():
    manager = User()

    manager.register(
        username=TEST_USER,
        email=TEST_MAIL,
        password=TEST_PASS,
    )

    response = client.get("/auth/verify", params={"email": TEST_MAIL})

    assert len(response.history) == 1
    assert response.history[0].status_code == 302
    assert response.url.path == "/"

    user = manager.one_or_none(TEST_MAIL).model_dump()

    expected_user = {
        "id": 1,
        "space_id": 999,
        "username": TEST_USER,
        "email": TEST_MAIL,
        "password": TEST_PASS,
        "last_login": None,
        "is_verified": True,
    }

    assert user == expected_user


def test_login():
    manager = User()

    manager.register(
        username=TEST_USER,
        email=TEST_MAIL,
        password=TEST_PASS,
    )

    manager.verify(email=TEST_MAIL)

    response = client.post(
        "/auth/login",
        json={
            "username": TEST_USER,
            "email": TEST_MAIL,
            "password": TEST_PASS,
        },
    )

    user = response.json()
    last_login = user.pop("last_login")

    expected_user = {
        "id": 1,
        "space_id": 999,
        "username": TEST_USER,
        "email": TEST_MAIL,
        "password": TEST_PASS,
        "is_verified": True,
    }

    assert user == expected_user
    assert last_login is not None
