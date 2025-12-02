import os
import socket
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch
from urllib.parse import quote

import pytest

from cloudisk.fs import utils
from cloudisk.fs.utils import (
    ask_remove_dir,
    ask_remove_file,
    ask_remove_path,
    attachment_content_disposition,
    get_mime_type,
    is_parent_path,
    is_subpath,
    iter_file_chunks,
    path_resolve,
)


@pytest.fixture
def mock_jpg_file():
    """Return a mocked jpg file."""
    fake_path = Path("mocked.jpg")
    mime_type = "image/jpeg"

    with (
        patch("pathlib.Path.is_file", return_value=True),
        patch.object(utils, "guess_mime", return_value=mime_type),
    ):
        yield fake_path, mime_type


@pytest.fixture
def mock_logger_error():
    with patch.object(utils.logger, "error") as mocked_logger:
        yield mocked_logger


@pytest.fixture
def mock_path_unlink():
    with patch("pathlib.Path.unlink") as mocked_unlink:
        yield mocked_unlink


@pytest.fixture
def mock_path_rmdir():
    with patch("pathlib.Path.rmdir") as mocked_path_rmdir:
        yield mocked_path_rmdir


@pytest.fixture
def mock_shutil_rmtree():
    with patch("shutil.rmtree") as mocked_rmtree:
        yield mocked_rmtree


def test_get_mime_type_from_file_returns_mime_type(mock_jpg_file: MagicMock):
    path, expected = mock_jpg_file
    result = get_mime_type(path)

    assert result == expected


def test_get_mime_type_from_path_returns_None(tmp_path: Path):
    expected = None
    result = get_mime_type(tmp_path)

    assert result == expected


def test_is_subpath_is_True(tmp_path: Path):
    previous_path = (tmp_path / "..").resolve()
    assert is_subpath(tmp_path, previous_path) is True


def test_is_subpath_is_False(tmp_path: Path):
    previous_path = (tmp_path / "..").resolve()
    assert is_subpath(previous_path, tmp_path) is False


def test_is_subpath_is_same(tmp_path: Path):
    assert is_subpath(tmp_path, tmp_path) is False


def test_is_parent_path_is_True(tmp_path: Path):
    previous_path = (tmp_path / "..").resolve()
    assert is_parent_path(previous_path, tmp_path) is True


def test_is_parent_path_is_False(tmp_path: Path):
    previous_path = (tmp_path / "..").resolve()
    assert is_parent_path(tmp_path, previous_path) is False


def test_is_parent_path_is_same(tmp_path: Path):
    assert is_parent_path(tmp_path, tmp_path) is False


def test_path_resolve_is_symlink(tmp_path: Path):
    symlink = tmp_path / "symlink"
    os.symlink(tmp_path, symlink)
    assert path_resolve(symlink) == symlink


def test_path_resolve_parent_is_symlink(tmp_path: Path):
    symlink = tmp_path / "symlink"
    os.symlink(tmp_path, symlink)
    tmp_file = symlink / "tmp_file"
    assert path_resolve(tmp_file) == tmp_file


def test_remove_file_logs_error_and_then_returns_False(
    mock_jpg_file: MagicMock,
    mock_logger_error: MagicMock,
):
    path, _ = mock_jpg_file

    responses = iter(("no", "n"))
    with patch("builtins.input", side_effect=lambda _: next(responses)):
        result = ask_remove_file(path)
        assert result is False
        mock_logger_error.assert_called_once()


def test_remove_file_returns_True(mock_jpg_file: MagicMock, mock_path_unlink: MagicMock):
    path, _ = mock_jpg_file

    responses = iter(("y"))
    with patch("builtins.input", side_effect=lambda _: next(responses)):
        result = ask_remove_file(path)
        assert result is True
        mock_path_unlink.assert_called_once()


def test_remove_dir_logs_error_and_then_returns_False(
    tmp_path: Path,
    mock_logger_error: MagicMock,
):
    responses = iter(("no", "n"))
    with patch("builtins.input", side_effect=lambda _: next(responses)):
        result = ask_remove_dir(tmp_path)
        assert result is False
        mock_logger_error.assert_called_once()


def test_remove_dir_when_empty_returns_True(tmp_path: Path, mock_path_rmdir: MagicMock):
    responses = iter(("y"))
    with patch("builtins.input", side_effect=lambda _: next(responses)):
        result = ask_remove_dir(tmp_path)
        assert result is True
        mock_path_rmdir.assert_called_once()


def test_remove_dir_when_not_empty_returns_True(
    tmp_path: Path,
    mock_shutil_rmtree: MagicMock,
):
    (tmp_path / "tmp_file").touch()

    responses = iter(("y"))
    with patch("builtins.input", side_effect=lambda _: next(responses)):
        result = ask_remove_dir(tmp_path)
        assert result is True
        mock_shutil_rmtree.assert_called_once()


def test_remove_path_when_file(mock_jpg_file: MagicMock, mock_path_unlink: MagicMock):
    responses = iter(("y"))
    with patch("builtins.input", side_effect=lambda _: next(responses)):
        path, _ = mock_jpg_file
        assert ask_remove_path(path) is True
        mock_path_unlink.assert_called_once()


def test_remove_path_when_path(tmp_path: Path, mock_path_rmdir: MagicMock):
    responses = iter(("y"))
    with patch("builtins.input", side_effect=lambda _: next(responses)):
        assert ask_remove_path(tmp_path) is True
        mock_path_rmdir.assert_called_once()


def test_remove_path_raises_exception(tmp_path: Path):
    socket_path = tmp_path / "tmp_socket.sock"
    exception_text = (
        f"{socket_path} already exists and is not a file or a directory. "
        "Please, remove it first."
    )

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(socket_path.as_posix())
    _ = s.makefile("rwb")

    with pytest.raises(Exception, match=exception_text) as exc_info:
        assert ask_remove_path(socket_path) == exc_info


def test_attachment_content_disposition_returns_file_name():
    file_name = "mocked_file"
    expected = f'attachment; filename="{file_name}"'

    assert attachment_content_disposition(file_name) == expected


def test_attachment_content_disposition_returns_formatted_filename():
    file_name = "mocked file"
    expected = f"attachment; filename*=utf-8''{quote(file_name)}"

    assert attachment_content_disposition(file_name) == expected


def test_iter_file_chunks_yield_chunk(tmp_path: Path):
    fake_data = b"123456789"
    chunk_size = 4

    with patch("builtins.open", mock_open(read_data=fake_data)) as mock_file:
        chunks = list(iter_file_chunks(tmp_path, chunk_size))
        expected = [
            fake_data[i : i + chunk_size] for i in range(0, len(fake_data), chunk_size)
        ]

        assert chunks == expected
        mock_file.assert_called_once()
