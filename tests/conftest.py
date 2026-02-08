import pytest

from cloudisk.context import Context
from cloudisk.vars import CLOUDISK_DB_FILE

TEST_USER = "test_user"
TEST_MAIL = "test@test.com"
TEST_PASS = "p4ssw0rd"


@pytest.fixture(autouse=True)
def fake_db(tmp_path, monkeypatch):
    tmp_db = tmp_path / CLOUDISK_DB_FILE

    monkeypatch.setattr("cloudisk.context.CLOUDISK_DB_PATH", tmp_db)
    monkeypatch.setattr("cloudisk.context.global_context", Context())

    monkeypatch.setattr("cloudisk.http.dependencies.CLOUDISK_DB_PATH", tmp_db)

    return tmp_db
