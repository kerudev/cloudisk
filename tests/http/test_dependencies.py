from pathlib import Path

import pytest
from fastapi import HTTPException

from cloudisk.http.dependencies import validate_path


@pytest.fixture(autouse=True)
def fake_root(tmp_path, monkeypatch) -> Path:
    (tmp_path / "file1.txt").write_text("Test 1")

    monkeypatch.setattr("cloudisk.fs.utils.CLOUDISK_ROOT", tmp_path)

    return tmp_path


@pytest.mark.asyncio
async def test_validate_path_ok():
    path = Path("file1.txt")

    result = await validate_path(path)

    assert result == path


@pytest.mark.asyncio
async def test_validate_path_ok_path_is_root():
    path = Path(".")

    result = await validate_path(path)

    assert result == path


@pytest.mark.asyncio
async def test_validate_path_err_403_parent_path(fake_root):
    path = Path("..")

    with pytest.raises(HTTPException) as exc_info:
        await validate_path(path)

    result = exc_info.value

    expected_path = (fake_root / path).resolve().as_posix()
    expected_detail = f"You are not allowed to retrieve {expected_path}"

    assert result.status_code == 403
    assert result.detail == expected_detail
