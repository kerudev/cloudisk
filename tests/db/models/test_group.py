import pytest

from cloudisk.db.models.group import Group, GroupModel


def test__init__(fake_context):
    manager = Group()

    assert manager.engine.url == fake_context.root.engine.url
    assert manager.scope == fake_context.root
    assert manager.model == GroupModel


def test_create_ok():
    manager = Group()

    group = manager.create(name="group")

    assert group.name == "group"


def test_create_raises_AlreadyExists():
    manager = Group()
    manager.create(name="group")

    with pytest.raises(Group.AlreadyExists):
        manager.create(name="group")


def test_one_or_none_returns_group():
    manager = Group()
    group = manager.create(name="group")

    assert manager.one_or_none(name="group") == group


def test_one_or_none_returns_None():
    assert Group().one_or_none(name="group") is None
