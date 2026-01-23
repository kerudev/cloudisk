import pytest

from cloudisk.db.models.user import User, UserModel

TEST_USER = "test_user"
TEST_MAIL = "test@test.com"
TEST_PASS = "p4ssw0rd"


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


def test_register_err_user_already_exists():
    manager = User()

    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    with pytest.raises(Exception):
        manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)


def test_verify():
    manager = User()

    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)
    user = manager.verify(email=TEST_MAIL)

    assert user.username == TEST_USER
    assert user.email == TEST_MAIL
    assert user.password == TEST_PASS
    assert user.last_login is None
    assert user.is_verified is True


def test_login_ok():
    manager = User()

    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)
    manager.verify(email=TEST_MAIL)
    user = manager.login(email=TEST_MAIL)

    assert user.username == TEST_USER
    assert user.email == TEST_MAIL
    assert user.password == TEST_PASS
    assert user.last_login is not None
    assert user.is_verified is True


def test_login_err_doesnt_exist():
    manager = User()

    with pytest.raises(Exception):
        manager.login(email=TEST_MAIL)


def test_login_err_user_is_not_verified():
    manager = User()
    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    with pytest.raises(Exception):
        manager.login(email=TEST_MAIL)


def test_exists_returns_True():
    manager = User()
    manager.register(username=TEST_USER, email=TEST_MAIL, password=TEST_PASS)

    assert manager.exists(email=TEST_MAIL) is True


def test_exists_returns_False():
    assert User().exists(email=TEST_MAIL) is False
