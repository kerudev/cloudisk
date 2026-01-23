import pytest

from cloudisk.vars import CLOUDISK_DB_FILE


@pytest.fixture(autouse=True)
def fake_db(tmp_path, monkeypatch):
    tmp_db = tmp_path / CLOUDISK_DB_FILE

    monkeypatch.setattr("cloudisk.db.models.base.CLOUDISK_DB_PATH", tmp_db)

    return tmp_db
