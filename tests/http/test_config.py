import json
from unittest.mock import Mock

import pytest

from cloudisk.http.config import general_exception_handler


@pytest.mark.asyncio
async def test_general_exception_handler():
    request = Mock()
    response = await general_exception_handler(request, Exception())

    assert response.status_code == 500

    content = json.loads(response.body)
    assert content["message"] == "Internal server error"
