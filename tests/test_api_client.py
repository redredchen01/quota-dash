import pytest
from unittest.mock import AsyncMock, patch
import httpx

from quota_dash.data.api_client import fetch_openai_usage


@pytest.mark.asyncio
async def test_fetch_openai_usage_success():
    mock_response = httpx.Response(
        200,
        json={"data": [{"results": [{"amount": {"value": 3.20}}]}]},
        request=httpx.Request("GET", "https://api.openai.com/v1/organization/usage"),
    )
    with patch("quota_dash.data.api_client.httpx.AsyncClient") as mock_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_cls.return_value = mock_client

        result = await fetch_openai_usage("test-api-key")
        assert result is not None
        assert result["usage_usd"] == 3.20


@pytest.mark.asyncio
async def test_fetch_openai_usage_403():
    mock_response = httpx.Response(
        403,
        text="Forbidden",
        request=httpx.Request("GET", "https://api.openai.com/v1/organization/usage"),
    )
    with patch("quota_dash.data.api_client.httpx.AsyncClient") as mock_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_cls.return_value = mock_client

        result = await fetch_openai_usage("test-api-key")
        assert result is None


@pytest.mark.asyncio
async def test_fetch_openai_usage_no_key():
    result = await fetch_openai_usage("")
    assert result is None
