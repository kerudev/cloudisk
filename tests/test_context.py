from cloudisk.context import Context
from cloudisk.vars import CLOUDISK_DB_FILE


def test__init__():
    context = Context()

    assert context._engine is None


def test_engine(tmp_path, monkeypatch):
    context = Context()
    tmp_db = tmp_path / CLOUDISK_DB_FILE

    monkeypatch.setattr("cloudisk.context.CLOUDISK_DB_PATH", tmp_db)

    assert str(context.engine.url) == f"sqlite:///{tmp_db}"


def test_reset():
    context = Context()

    assert context._engine is None
