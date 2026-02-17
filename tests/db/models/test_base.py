import pytest

from cloudisk.db.models.base import ModelManager


def test__init__(fake_db):
    manager = ModelManager()

    assert str(manager.engine.url) == f"sqlite:///{fake_db}"
    assert manager.model is None


def test_table_exists():
    with pytest.raises(AttributeError):
        ModelManager().table_exists()
