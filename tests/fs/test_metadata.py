from pathlib import Path

import pytest

from cloudisk.db.models.metadata import Metadata, MetadataManager
from cloudisk.vars import METADATA_FILE


@pytest.fixture(autouse=True)
def fake_db(tmp_path, monkeypatch):
    tmp_db = tmp_path / METADATA_FILE

    monkeypatch.setattr("cloudisk.db.models.metadata.METADATA_PATH", tmp_db)

    return tmp_db


@pytest.fixture(autouse=True)
def fake_root(tmp_path, monkeypatch):
    file1 = tmp_path / "file1.txt"
    file1.write_text("Test 1")

    file2 = tmp_path / "file2.fake"
    file2.write_text("Test 2")

    link1 = tmp_path / "link1.txt"
    link1.symlink_to(tmp_path / "file1.txt")

    dir1 = tmp_path / "dir1"
    dir1.mkdir()

    dir1_file1 = dir1 / "dir1_file1.txt"
    dir1_file1.write_text("Test Dir1 1")

    dir1_file2 = dir1 / "dir1_file2.txt"
    dir1_file2.write_text("Test Dir1 2")

    monkeypatch.setattr("cloudisk.fs.utils.CLOUDISK_ROOT", tmp_path)

    file_list = [
        file1,
        file2,
        link1,
        dir1,
        dir1_file1,
        dir1_file2,
    ]

    manager = MetadataManager()

    for file in file_list:
        manager.create(file)

    return tmp_path


def test__init__(fake_db):
    manager = MetadataManager()

    assert str(manager.engine.url) == f"sqlite:///{fake_db}"
    assert manager.model == Metadata


def test_get_engine(fake_db):
    engine = MetadataManager.get_engine()

    assert str(engine.url) == f"sqlite:///{fake_db}"


def test_available_paths_table_exists(fake_root):
    paths = MetadataManager().available_paths

    expected_paths = [
        fake_root / "file1.txt",
        fake_root / "file2.fake",
        fake_root / "link1.txt",
        fake_root / "dir1",
        fake_root / "dir1" / "dir1_file1.txt",
        fake_root / "dir1" / "dir1_file2.txt",
    ]

    for path in paths:
        assert Path(path) in expected_paths


def test_available_paths_table_doesnt_exist():
    manager = MetadataManager()
    manager.model.__table__.drop(manager.engine)

    paths = manager.available_paths

    assert paths == []


def test_select(fake_root):
    path = fake_root / "file1.txt"

    metadata = MetadataManager().select(path)

    assert metadata.path == str(path)
    assert metadata.size == path.stat().st_size
    assert metadata.content_type == ""


def test_create_ok(fake_root):
    path = fake_root / "new1.txt"
    path.write_text("Content")

    metadata = MetadataManager().create(path)

    assert metadata.path == str(path)
    assert metadata.size == path.stat().st_size
    assert metadata.content_type == ""


def test_create_err_non_unique_path(fake_root):
    path = fake_root / "file1.txt"
    metadata = MetadataManager().create(path)

    assert metadata is None


def test_remove(fake_root):
    manager = MetadataManager()
    path = fake_root / "file1.txt"

    manager.remove(path)

    metadata = manager.select(path)

    assert metadata.available is False


def test_increment_downloads(fake_root):
    manager = MetadataManager()
    path = fake_root / "file1.txt"

    manager.increment_downloads(path)

    metadata = manager.select(path)

    assert metadata.downloads == 1
