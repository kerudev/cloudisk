import pytest

from cloudisk.db.models.space import Space, SpaceModel


def test__init__(fake_context):
    manager = Space()

    assert manager.engine.url == fake_context.root.engine.url
    assert manager.scope == fake_context.root
    assert manager.model == SpaceModel


def test_create_ok():
    manager = Space()

    space = manager.create(name="test", protect=True)

    assert space.name == "test"
    assert space.protect is True
    assert space.used is False


def test_create_raises_AlreadyExists():
    manager = Space()

    manager.create(name="test", protect=True)

    with pytest.raises(Space.AlreadyExists):
        manager.create(name="test", protect=True)


def test_use():
    manager = Space()

    manager.create(name="test", protect=True)
    space = manager.use(name="test")

    assert space.name == "test"
    assert space.protect is True
    assert space.used is True


def test_use_change_used():
    manager = Space()

    manager.create(name="test1", protect=True)
    manager.create(name="test2", protect=True)
    manager.use(name="test1")
    space = manager.use(name="test2")

    assert space.name == "test2"
    assert space.protect is True
    assert space.used is True


def test_use_when_space_is_already_used():
    manager = Space()

    manager.create(name="test1", protect=True)
    manager.use(name="test1")
    space = manager.use(name="test1")

    assert space.name == "test1"
    assert space.protect is True
    assert space.used is True


def test_get_used():
    manager = Space()

    manager.create(name="test", protect=True)
    manager.use(name="test")
    space = manager.get_used()

    assert space.name == "test"
    assert space.protect is True
    assert space.used is True


def test_list():
    manager = Space()

    manager.create(name="test", protect=True)

    result = manager.list()
    execpted = ["test"]

    assert result == execpted
