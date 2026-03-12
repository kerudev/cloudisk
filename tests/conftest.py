import pytest

from cloudisk.tools import Context, Scope
from cloudisk.vars import CLOUDISK_DB_FILE

TEST_USER = "test_user"
TEST_MAIL = "test@test.com"
TEST_PASS = "p4ssw0rd"


@pytest.fixture(autouse=True)
def fake_db(tmp_path, monkeypatch):
    tmp_db = tmp_path / CLOUDISK_DB_FILE
    monkeypatch.setattr("cloudisk.http.dependencies.CLOUDISK_DB_PATH", tmp_db)

    return tmp_db


@pytest.fixture(autouse=True)
def fake_context(tmp_path, monkeypatch, fake_db):
    monkeypatch.setattr("cloudisk.vars.CLOUDISK_ROOT", tmp_path)
    monkeypatch.setattr("cloudisk.tools.settings.CLOUDISK_ROOT", tmp_path)

    test_scope = Scope("root", engine_path=fake_db)

    test_scope.extras["space_id"] = 999
    test_scope.extras["space_name"] = "test_space"

    (tmp_path / test_scope.extras["space_name"]).mkdir()

    test_context = Context(scopes=[test_scope])

    monkeypatch.setattr("cloudisk.globals.context", test_context)
    monkeypatch.setattr("cloudisk.fs.utils.context", test_context)
    monkeypatch.setattr("cloudisk.db.models.base.context", test_context)

    return test_context
