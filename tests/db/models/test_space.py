import pytest

from cloudisk.db.models.space import Space, SpaceModel


def test__init__(fake_context):
    manager = Space()

    assert manager.engine.url == fake_context.root.engine.url
    assert manager.scope == fake_context.root
    assert manager.model == SpaceModel


def test_create_ok():
    manager = Space()

    name = "test"
    protect = True

    space = manager.create(name=name, protect=protect)

    assert space.name == name
    assert space.protect is True


def test_create_raises_AlreadyExists():
    manager = Space()

    manager.create(name="test", protect=True)

    with pytest.raises(Space.AlreadyExists):
        manager.create(name="test", protect=True)


def test_list():
    manager = Space()

    manager.create(name="test", protect=True)

    result = manager.list()
    execpted = ["test"]

    assert result == execpted
