import pytest

from cloudisk.db.models.base import ModelManager


def test__init__(fake_context):
    manager = ModelManager()

    assert manager.engine.url == fake_context.root.engine.url
    assert manager.scope == fake_context.root
    assert manager.model is None


def test_table_exists():
    with pytest.raises(AttributeError):
        ModelManager().table_exists()
