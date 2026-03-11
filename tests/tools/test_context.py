from cloudisk.tools.scope import Scope
from cloudisk.vars import CLOUDISK_DB_FILE


def test__init__(tmp_path):
    tmp_db = tmp_path / CLOUDISK_DB_FILE

    instance = Scope("test", engine_path=tmp_db)

    assert instance.name == "test"
    assert instance.engine_path == tmp_db
    assert instance.settings_path is None
    assert instance.settings_module is None

    assert instance.extras == {}
    assert instance._engine is None
    assert instance._settings is None


def test_engine(tmp_path):
    tmp_db = tmp_path / CLOUDISK_DB_FILE
    instance = Scope("test", engine_path=tmp_db)

    assert str(instance.engine.url) == f"sqlite:///{tmp_db}"
    assert instance._engine is not None


def test_cleanup(tmp_path):
    tmp_db = tmp_path / CLOUDISK_DB_FILE
    instance = Scope("test", engine_path=tmp_db)

    instance.set_engine()
    instance.cleanup()

    assert instance._engine is None
