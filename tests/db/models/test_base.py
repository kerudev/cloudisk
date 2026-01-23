import pytest

from cloudisk.db.models.base import ModelManager


def test__init__(fake_db):
    manager = ModelManager()

    assert str(manager.engine.url) == f"sqlite:///{fake_db}"
    assert not hasattr(manager, "model")


# Abstract


def test_table_exists(fake_db):
    with pytest.raises(AttributeError):
        ModelManager().table_exists()


# Public


def test_get_engine(fake_db):
    engine = ModelManager.get_engine()

    assert str(engine.url) == f"sqlite:///{fake_db}"
