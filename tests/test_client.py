from __future__ import annotations

import pytest

from mosir_sdk import DEFAULT_ENDPOINT, AsyncMosirClient


@pytest.mark.asyncio
async def test_client_uses_default_endpoint() -> None:
    client = AsyncMosirClient()
    try:
        assert client.endpoint == DEFAULT_ENDPOINT
        assert client.token is None
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_pythonic_get_post_request() -> None:
    async with AsyncMosirClient() as client:
        data = await client.get_post(post_id="VLO8u7UXqclQ7byjfMEX0")

    assert data["getPost"]["id"] == "VLO8u7UXqclQ7byjfMEX0"
    assert data["getPost"]["author"]["username"] == "leemiyinghao"
