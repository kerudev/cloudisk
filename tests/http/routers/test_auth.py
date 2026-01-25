from fastapi.testclient import TestClient

from cloudisk.db.models.user import User
from cloudisk.http.config import app
from tests.conftest import TEST_MAIL, TEST_PASS, TEST_USER

client = TestClient(app)


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
        "username": TEST_USER,
        "email": TEST_MAIL,
        "password": TEST_PASS,
        "last_login": None,
        "is_verified": False,
    }

    assert user == expected_user


def test_verify():
    User().register(
        username=TEST_USER,
        email=TEST_MAIL,
        password=TEST_PASS,
    )

    response = client.post(
        "/auth/verify",
        json={
            "username": TEST_USER,
            "email": TEST_MAIL,
            "password": TEST_PASS,
        },
    )

    user = response.json()

    expected_user = {
        "id": 1,
        "username": TEST_USER,
        "email": TEST_MAIL,
        "password": TEST_PASS,
        "last_login": None,
        "is_verified": True,
    }

    assert user == expected_user


def test_login():
    User().register(
        username=TEST_USER,
        email=TEST_MAIL,
        password=TEST_PASS,
    )

    User().verify(
        email=TEST_MAIL,
        password=TEST_PASS,
    )

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
        "username": TEST_USER,
        "email": TEST_MAIL,
        "password": TEST_PASS,
        "is_verified": True,
    }

    assert user == expected_user
    assert last_login is not None
