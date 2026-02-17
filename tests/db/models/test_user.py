from unittest.mock import MagicMock

import pytest

from cloudisk.db.models.user import User, UserModel
from tests.conftest import TEST_MAIL, TEST_PASS, TEST_USER


@pytest.fixture(autouse=True)
def mock_send_verify_email(monkeypatch, request):
    if request.node.get_closest_marker("no_mock"):
        return

    monkeypatch.setattr(
        "cloudisk.db.models.user.User._send_verify_email", lambda _, __: ...
    )


def test__init__(fake_db):
    manager = User()

    assert str(manager.engine.url) == f"sqlite:///{fake_db}"
    assert manager.model == UserModel


def test_register_ok():
    manager = User()

    user = manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    assert user.username == TEST_USER
    assert user.email == TEST_MAIL
    assert user.password == TEST_PASS
    assert user.last_login is None
    assert user.is_verified is False


def test_register_raises_UsernameExists():
    manager = User()
    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    with pytest.raises(User.UsernameExists):
        manager.register(username=TEST_USER, email="fake@test.com", password=TEST_PASS)


def test_register_raises_EmailExists():
    manager = User()
    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    with pytest.raises(User.EmailExists):
        manager.register(username="test_user2", email=TEST_MAIL, password=TEST_PASS)


def test_verify_ok():
    manager = User()
    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    user = manager.verify(email=TEST_MAIL)

    assert user.username == TEST_USER
    assert user.email == TEST_MAIL
    assert user.password == TEST_PASS
    assert user.last_login is None
    assert user.is_verified is True


def test_verify_raises_DoesNotExist():
    manager = User()

    with pytest.raises(User.DoesNotExist):
        manager.verify(email=TEST_MAIL)


def test_login_ok():
    manager = User()

    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)
    manager.verify(email=TEST_MAIL)
    user = manager.login(email=TEST_MAIL, password=TEST_PASS)

    assert user.username == TEST_USER
    assert user.email == TEST_MAIL
    assert user.password == TEST_PASS
    assert user.last_login is not None
    assert user.is_verified is True


def test_login_raises_DoesNotExist():
    manager = User()

    with pytest.raises(User.DoesNotExist):
        manager.login(email=TEST_MAIL, password=TEST_PASS)


def test_login_raises_NotVerified():
    manager = User()
    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    with pytest.raises(User.NotVerified):
        manager.login(email=TEST_MAIL, password=TEST_PASS)


def test_login_raises_IncorrectPassword():
    manager = User()
    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)
    manager.verify(email=TEST_MAIL)

    with pytest.raises(User.IncorrectPassword):
        manager.login(email=TEST_MAIL, password="incorrect_password")


def test_one_or_none_returns_user():
    manager = User()
    user = manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    assert manager.one_or_none(email=TEST_MAIL) == user


def test_one_or_none_returns_None():
    assert User().one_or_none(email=TEST_MAIL) is None


@pytest.mark.no_mock
def test_send_verify_email_ok(monkeypatch):
    mock_smtp = MagicMock()

    monkeypatch.setattr("cloudisk.db.models.user.smtplib.SMTP", mock_smtp)
    monkeypatch.setenv("CLOUDISK_EMAIL_FROM", TEST_MAIL)

    User()._send_verify_email(email=TEST_MAIL)

    mock_smtp.return_value.__enter__.return_value.send_message.assert_called_once()


@pytest.mark.no_mock
def test_send_verify_email_raises_Exception():
    with pytest.raises(Exception):
        User()._send_verify_email(email=TEST_MAIL)
