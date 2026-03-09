from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from cloudisk.db.models import Metadata
from cloudisk.http.config import app
from cloudisk.http.routers import files
from cloudisk.http.routers.files import _download_files, _list_files
from cloudisk.vars import MB_1

client = TestClient(app)


@pytest.fixture(autouse=True)
def fake_root(tmp_path, monkeypatch) -> Path:
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

    fake_metadata = Metadata()

    for file in file_list:
        fake_metadata.create(file)

    return tmp_path


@pytest.fixture
def endpoint_download():
    with patch.object(files, "_download_files", wraps=files._download_files) as mock:
        yield mock


@pytest.fixture
def endpoint_list():
    with patch.object(files, "_list_files", wraps=files._list_files) as mock:
        yield mock


def test_get_files_ok(endpoint_download, endpoint_list):
    response = client.get("/files")

    assert response.status_code == 200
    assert response.json() == {
        "files": ["dir1", "file1.txt", "file2.fake", "link1.txt"],
        "isRoot": True,
    }

    endpoint_download.assert_not_called()
    endpoint_list.assert_called_once()


def test_get_files_ok_with_dir_path(endpoint_download, endpoint_list):
    response = client.get("/files", params={"path": "dir1"})

    assert response.status_code == 200
    assert response.json() == {
        "files": ["dir1_file1.txt", "dir1_file2.txt"],
        "isRoot": False,
    }

    endpoint_download.assert_not_called()
    endpoint_list.assert_called_once()


def test_get_files_ok_with_unavailable_path(endpoint_download, endpoint_list):
    fake_metadata = Metadata()

    fake_metadata.model.__table__.drop(fake_metadata.engine)

    response = client.get("/files")

    assert response.status_code == 200
    assert response.json() == {
        "files": [],
        "isRoot": True,
    }

    endpoint_download.assert_not_called()
    endpoint_list.assert_called_once()


def test_get_files_ok_no_available_paths(endpoint_download, endpoint_list, fake_root):
    fake_metadata = Metadata()
    fake_metadata.remove(fake_root / "dir1")
    fake_metadata.remove(fake_root / "file1.txt")
    fake_metadata.remove(fake_root / "file2.fake")
    fake_metadata.remove(fake_root / "link1.txt")

    response = client.get("/files")

    assert response.status_code == 200
    assert response.json() == {
        "files": [],
        "isRoot": True,
    }

    endpoint_download.assert_not_called()
    endpoint_list.assert_called_once()


@pytest.mark.asyncio
async def test_list_files_500_path_is_file(fake_root):
    path = fake_root / "file1.txt"

    with pytest.raises(HTTPException) as exc_info:
        await _list_files(path)

    response = exc_info.value

    assert response.status_code == 500
    assert path.as_posix() in response.detail


def test_get_files_ok_with_file_path_small_file(endpoint_download, endpoint_list):
    response = client.get("/files", params={"path": "file1.txt"})

    assert response.status_code == 200
    assert response.headers.get("content-type") == "text/plain; charset=utf-8"
    assert (
        response.headers.get("content-disposition") == 'attachment; filename="file1.txt"'
    )

    endpoint_download.assert_called_once()
    endpoint_list.assert_not_called()


def test_get_files_err_404_path_doesnt_exist(endpoint_download, endpoint_list, fake_root):
    response = client.get("/files", params={"path": "fake"})

    assert response.status_code == 404

    content = response.json()
    expected_path = (fake_root / "fake").as_posix()

    assert content["detail"] == f"{expected_path} path does not exist"

    endpoint_download.assert_not_called()
    endpoint_list.assert_called_once()


@pytest.mark.asyncio
async def test_download_files_ok_with_file_path_large_file(fake_root):
    with patch.object(files, "Path") as mock_path:
        path = fake_root / "file3.txt"

        mock_path.name = "file3.txt"
        mock_path._str = str(path)
        mock_path.is_file.return_value = False
        mock_path.stat.return_value.st_size = MB_1 * 200

        response = await _download_files(mock_path)

    assert response.status_code == 206
    assert response.headers.get("content-length") == str(MB_1 * 200)
    assert (
        response.headers.get("content-disposition") == 'attachment; filename="file3.txt"'
    )


def test_upload_file_ok_one_file():
    files = [
        ("files", ("file3.md", b"Test 3", "text/plain")),
    ]

    response = client.post("/files", files=files)

    assert response.status_code == 200
    assert response.json() == {
        "files": ["dir1", "file1.txt", "file2.fake", "file3.md", "link1.txt"],
        "isRoot": True,
    }


def test_upload_file_ok_many_files():
    files = [
        ("files", ("file3.md", b"Test 3", "text/plain")),
        ("files", ("file4.txt", b"Test 4", "text/plain")),
        ("files", ("file5.csv", b"Test 5", "text/plain")),
    ]

    response = client.post("/files", files=files)

    assert response.status_code == 200
    assert response.json() == {
        "files": [
            "dir1",
            "file1.txt",
            "file2.fake",
            "file3.md",
            "file4.txt",
            "file5.csv",
            "link1.txt",
        ],
        "isRoot": True,
    }


def test_upload_file_err_metadata_creation_error():
    files = [
        ("files", ("file3.md", b"Test 3", "text/plain")),
    ]

    with patch.object(Metadata, "create") as mock_metadata:
        mock_metadata.side_effect = Exception("not in database")

        response = client.post("/files", files=files)

    assert response.status_code == 200
    assert response.json() == {
        "files": [
            "dir1",
            "file1.txt",
            "file2.fake",
            "link1.txt",
        ],
        "isRoot": True,
    }


def test_upload_file_ok_existing_file_name():
    files = [
        ("files", ("file1.txt", b"Test 3", "text/plain")),
    ]

    response = client.post("/files", files=files)

    assert response.status_code == 200
    assert response.json() == {
        "files": ["dir1", "file1.txt", "file1_1.txt", "file2.fake", "link1.txt"],
        "isRoot": True,
    }


def test_upload_file_err_422_no_files():
    response = client.post("/files")

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "files"],
                "msg": "Field required",
                "input": None,
            }
        ]
    }


def test_upload_file_err_403_subpath(fake_root):
    files = [
        ("files", ("../file1.txt", b"", "text/plain")),
    ]

    response = client.post("/files", files=files)

    assert response.status_code == 403

    content = response.json()
    expected_path = (fake_root / "../file1.txt").as_posix()

    assert content["detail"] == f"You are not allowed to create {expected_path}"


def test_delete_file_ok_file(fake_root):
    path = fake_root / "file1.txt"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 200
    assert path.exists()

    content = response.json()
    assert content["message"] == f"{path.as_posix()} deleted correctly"


def test_delete_file_ok_dir(fake_root):
    path = fake_root / "dir1"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 200
    assert path.exists()

    content = response.json()
    assert content["message"] == f"{path.as_posix()} deleted correctly"


def test_delete_file_ok_link(fake_root):
    path = fake_root / "link1.txt"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 200
    assert path.exists()

    content = response.json()
    assert content["message"] == f"{path.as_posix()} deleted correctly"


def test_delete_file_err_403_subpath(fake_root):
    path = fake_root / "../file1.txt"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 403
    assert not path.exists()

    content = response.json()
    assert content["detail"] == f"You are not allowed to delete {path.as_posix()}"


def test_delete_file_err_404_path_doesnt_exist(fake_root):
    path = fake_root / "fake.txt"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 404
    assert not path.exists()

    content = response.json()
    assert content["detail"] == f"File at {path.as_posix()} not found"


def test_delete_file_err_500_path_not_removed(fake_root):
    path = fake_root / "file1.txt"

    with patch.object(Metadata, "remove") as mock_metadata:
        mock_metadata.side_effect = Exception("not in database")

        response = client.delete("/files", params={"path": path})

    assert response.status_code == 500
    assert path.exists()

    content = response.json()
    assert content["detail"] == f"{path.as_posix()} could not be deleted: not in database"
