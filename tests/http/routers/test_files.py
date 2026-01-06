from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from cloudisk.http.config import app
from cloudisk.http.routers import files
from cloudisk.http.routers.files import _download_files, _list_files
from cloudisk.vars import MB_1

client = TestClient(app)


@pytest.fixture(autouse=True)
def fake_root(tmp_path, monkeypatch):
    (tmp_path / "file1.txt").write_text("Test 1")
    (tmp_path / "file2.fake").write_text("Test 2")

    (tmp_path / "link1.txt").symlink_to(tmp_path / "file1.txt")

    dir1 = tmp_path / "dir1"
    dir1.mkdir()

    (dir1 / "dir1_file1.txt").write_text("Test Dir1 1")
    (dir1 / "dir1_file2.txt").write_text("Test Dir1 2")

    monkeypatch.setattr("cloudisk.fs.utils.CLOUDISK_ROOT", tmp_path)
    monkeypatch.setattr("cloudisk.http.dependencies.CLOUDISK_ROOT", tmp_path)
    monkeypatch.setattr("cloudisk.http.routers.files.CLOUDISK_ROOT", tmp_path)

    return tmp_path


@pytest.fixture
def endpoint_download():
    with patch.object(
        files, "_download_files", wraps=files._download_files
    ) as mock_endpoint:
        yield mock_endpoint


@pytest.fixture
def endpoint_list():
    with patch.object(files, "_list_files", wraps=files._list_files) as mock_endpoint:
        yield mock_endpoint


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


@pytest.mark.asyncio
async def test_list_files_500_path_is_file(fake_root):
    with pytest.raises(HTTPException) as exc_info:
        await _list_files(fake_root / "file1.txt")

    response = exc_info.value

    assert response.status_code == 500
    assert "Errno 20" in response.detail


def test_get_files_ok_with_file_path_mime_exception(endpoint_download, endpoint_list):
    with patch.object(files, "get_mime_type") as mock_mime:
        mock_mime.side_effect = TypeError
        response = client.get("/files", params={"path": "file2.fake"})

    assert response.status_code == 200
    assert response.headers.get("content-type") == "text/plain; charset=utf-8"
    assert (
        response.headers.get("content-disposition") == 'attachment; filename="file2.fake"'
    )

    endpoint_download.assert_called_once()
    endpoint_list.assert_not_called()


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
    assert content["detail"] == f"{fake_root / 'fake'} path does not exist"

    endpoint_download.assert_not_called()
    endpoint_list.assert_called_once()


@pytest.mark.asyncio
async def test_download_files_ok_with_file_path_large_file():
    with patch.object(files, "Path") as mock_path:
        mock_path.name = "file3.txt"
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
    assert (
        content["detail"] == f'You are not allowed to create {fake_root / "../file1.txt"}'
    )


def test_delete_file_ok_file(fake_root):
    path = fake_root / "file1.txt"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 200
    assert not path.exists()

    content = response.json()
    assert content["message"] == f"{path} deleted correctly"


def test_delete_file_ok_dir(fake_root):
    path = fake_root / "dir1"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 200
    assert not path.exists()

    content = response.json()
    assert content["message"] == f"{path} deleted correctly"


def test_delete_file_ok_link(fake_root):
    path = fake_root / "link1.txt"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 200
    assert not path.exists()

    content = response.json()
    assert content["message"] == f"{path} deleted correctly"


def test_delete_file_err_403_subpath(fake_root):
    path = fake_root / "../file1.txt"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 403
    assert not path.exists()

    content = response.json()
    assert content["detail"] == f"You are not allowed to delete {path}"


def test_delete_file_err_404_path_doesnt_exist(fake_root):
    path = fake_root / "fake.txt"

    response = client.delete("/files", params={"path": path})

    assert response.status_code == 404
    assert not path.exists()

    content = response.json()
    assert content["detail"] == f"File at {path} not found"


# def test_delete_file_err_400_not_deleted(fake_root, monkeypatch):
#     path = fake_root / "block"

#     monkeypatch.setattr(path, "is_symlink", lambda: False)
#     monkeypatch.setattr(path, "is_file", lambda: False)
#     monkeypatch.setattr(path, "is_dir", lambda: False)

#     response = client.delete("/files", params={"path": path})

#     assert response.status_code == 400
#     assert not path.exists()

#     content = response.json()
#     assert content["detail"] == f"{path} deleted correctly"
