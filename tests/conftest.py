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

    monkeypatch.setattr("cloudisk.tools.scope.CLOUDISK_ROOT", tmp_path)

    test_context = Context(scopes=[Scope("root", engine_path=tmp_db)])
    test_context.root.update_space()

    monkeypatch.setattr("cloudisk.globals.context", test_context)

    yield tmp_db

    # del test_context
