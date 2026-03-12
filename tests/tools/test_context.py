from cloudisk.tools.context import Context
from cloudisk.tools.scope import Scope
from cloudisk.vars import CLOUDISK_DB_FILE


def test__init__(tmp_path):
    tmp_db = tmp_path / CLOUDISK_DB_FILE

    instance = Context(scopes=[Scope("test", engine_path=tmp_db)])

    assert len(instance.scopes) == 1
    assert "test" in instance.scopes


def test__init__no_scope():
    instance = Context()

    assert len(instance.scopes) == 0
    assert instance.scopes == {}


def test_add_scope(tmp_path):
    tmp_db = tmp_path / CLOUDISK_DB_FILE

    instance = Context()
    instance.add_scope(Scope("test", engine_path=tmp_db))

    assert len(instance.scopes) == 1
    assert "test" in instance.scopes


def test_get_scope(tmp_path):
    tmp_db = tmp_path / CLOUDISK_DB_FILE

    instance = Context(scopes=[Scope("test", engine_path=tmp_db)])

    assert instance.test == instance.scopes["test"]


def test_drop_scope(tmp_path):
    tmp_db = tmp_path / CLOUDISK_DB_FILE

    instance = Context(scopes=[Scope("test", engine_path=tmp_db)])
    instance.drop_scope("test")

    assert len(instance.scopes) == 0
    assert instance.scopes == {}


def test_drop_scope_when_scopes_is_empty():
    instance = Context()
    instance.drop_scope("test")

    assert len(instance.scopes) == 0
    assert instance.scopes == {}
