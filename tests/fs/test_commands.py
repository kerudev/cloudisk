import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from cloudisk.fs import commands
from cloudisk.fs.commands import (
    _try_link,
    create_space,
    init_cloudisk_root,
    link_path,
    unlink_path,
)


@pytest.fixture(autouse=True)
def fake_root(tmp_path, monkeypatch) -> Path:
    fake_path = tmp_path / "root"
    fake_path.mkdir()

    monkeypatch.setattr("cloudisk.fs.commands.CLOUDISK_ROOT", fake_path)

    return fake_path


def test_init_cloudisk_root_ok(fake_root):
    fake_root.rmdir()

    with patch.object(commands, "ask_remove_path", return_value=True):
        result = init_cloudisk_root()

    assert result is True
    assert fake_root.exists()
    assert fake_root.is_dir()


def test_init_cloudisk_root_err(fake_root):
    with patch.object(commands, "ask_remove_path", return_value=False):
        result = init_cloudisk_root()

    assert result is False
    assert fake_root.exists()
    assert fake_root.is_dir()


def test_try_link_ok(fake_root):
    src = fake_root / "src"
    dst = fake_root / "dst"

    src.mkdir()

    _try_link(src, dst)
    _try_link(src, dst)

    assert dst.is_symlink()
    assert dst.resolve() == src
    assert dst.resolve().is_dir()


def test_try_link_err(fake_root):
    src = fake_root / "src"
    dst = fake_root / "dst"

    src.mkdir()

    _try_link(src, dst)

    assert dst.is_symlink()
    assert dst.resolve() == src


def test_try_link_raises_OSError(fake_root):
    src = fake_root / "src"
    dst = fake_root / "dst"

    src.mkdir()

    with pytest.raises(OSError) as exc_info:
        with patch.object(os, "symlink", side_effect=OSError):
            _try_link(src, dst)

    if os.name == "nt":
        assert "Developer Mode" in str(exc_info.value)

    assert not dst.is_symlink()
    assert not dst.resolve() == src


def test_link_path_ok_not_recursive_path_is_file(tmp_path, fake_root):
    file = tmp_path / "file1.txt"
    file.write_text("Content")

    link_path(file, recursive=False)

    link = fake_root / "file1.txt"

    assert link.exists()
    assert link.is_symlink()
    assert link.resolve() == file
    assert link.resolve().is_file()


def test_link_path_ok_not_recursive_path_is_dir(tmp_path, fake_root):
    dir = tmp_path / "dir"
    dir.mkdir()

    file = dir / "file1.txt"
    file.write_text("Content")

    link_path(dir, recursive=False)

    link = fake_root / "dir"

    assert link.exists()
    assert link.is_symlink()
    assert link.resolve() == dir
    assert link.resolve().is_dir()


def test_link_path_ok_recursive(tmp_path, fake_root):
    dir = tmp_path / "dir"
    dir.mkdir()

    file = dir / "file1.txt"
    file.write_text("Content")

    link_path(dir, recursive=True)

    link = fake_root / "file1.txt"

    assert link.exists()
    assert link.is_symlink()
    assert link.resolve() == file
    assert link.resolve().is_file()


def test_link_path_err_path_doesnt_exist(fake_root):
    path = fake_root / "missing"

    link_path(path)

    assert not path.exists()
    assert not path.is_symlink()


def test_link_path_err_dst_exists(tmp_path, fake_root):
    (fake_root / "file1.txt").write_text("Content")

    file = tmp_path / "file1.txt"
    file.write_text("Content")

    link_path(file)

    link = fake_root / "file1.txt"

    assert link.exists()
    assert not link.is_symlink()
    assert not link.resolve() == file


def test_unlink_path_ok(tmp_path, fake_root):
    file = tmp_path / "file1.txt"
    file.write_text("Content")

    link = fake_root / "file1.txt"

    os.symlink(file, link, target_is_directory=True)
    unlink_path(link)

    assert not link.exists()
    assert not link.is_symlink()


def test_unlink_path_err_path_is_file(fake_root):
    path = fake_root / "file1.txt"
    path.write_text("Content")

    unlink_path(path)

    assert path.exists()
    assert not path.is_symlink()


def test_unlink_path_err_path_doesnt_exist(fake_root):
    path = fake_root / "missing"

    unlink_path(path)

    assert not path.exists()
    assert not path.is_symlink()


def test_create_space(fake_root):
    space_name = "test"
    space_path = fake_root / space_name

    create_space(name=space_name, protect=True)

    assert space_path.exists()


def test_create_space_root_doenst_exist(fake_root):
    shutil.rmtree(fake_root)

    space_name = "test"
    space_path = fake_root / space_name

    create_space(name=space_name, protect=True)

    assert space_path.exists()


def test_create_space_ask_remove_dir_is_False(fake_root):
    space_name = "test"
    space_path = fake_root / space_name

    create_space(name=space_name, protect=True)

    with patch.object(commands, "ask_remove_dir", return_value=False):
        create_space(name=space_name, protect=True)

    assert space_path.exists()
