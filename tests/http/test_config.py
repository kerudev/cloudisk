import json
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from cloudisk.db.models import Metadata, User
from cloudisk.http.config import (
    general_exception_handler,
    metadata_exception_handler,
    user_exception_handler,
)


@pytest.mark.asyncio
async def test_general_exception_handler():
    request = Mock()
    response = await general_exception_handler(
        request,
        Exception("Internal server error"),
    )

    assert response.status_code == 500

    content = json.loads(response.body)
    assert content["message"] == "Internal server error"


@pytest.mark.asyncio
async def test_user_exception_handler():
    request = Mock()

    with pytest.raises(HTTPException) as exc_info:
        await user_exception_handler(
            request,
            User.Error("Internal server error"),
        )

    response = exc_info.value

    assert response.status_code == 400
    assert response.detail == "Internal server error"


@pytest.mark.asyncio
async def test_metadata_exception_handler():
    request = Mock()

    with pytest.raises(HTTPException) as exc_info:
        await metadata_exception_handler(
            request,
            Metadata.Error("Internal server error"),
        )

    response = exc_info.value

    assert response.status_code == 400
    assert response.detail == "Internal server error"
