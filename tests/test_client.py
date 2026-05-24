from __future__ import annotations

import json

import httpx
import pytest

from mosir_sdk import (
    DEFAULT_ENDPOINT,
    AsyncMosirClient,
    OPERATION_REGISTRY,
    get_preview_image_url,
    select_media_file,
)


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


@pytest.mark.asyncio
async def test_operation_method_uses_registry() -> None:
    async with AsyncMosirClient() as client:
        data = await client.operation("get_post", post_id="VLO8u7UXqclQ7byjfMEX0")

    assert "get_post" in OPERATION_REGISTRY
    assert data["getPost"]["id"] == "VLO8u7UXqclQ7byjfMEX0"


def test_select_media_file_prefers_quality_profile() -> None:
    media = {
        "files": [
            {"profile": "THUMBNAIL", "url": "https://example.com/thumb.jpg"},
            {"profile": "QUALITY", "url": "https://example.com/quality.mp4"},
        ]
    }

    selected = select_media_file(media)

    assert selected is not None
    assert selected["url"] == "https://example.com/quality.mp4"


def test_get_preview_image_url_uses_ogi_path() -> None:
    url = get_preview_image_url("post", "VLO8u7UXqclQ7byjfMEX0")
    assert url == "https://beta.mosir.app/ogi/postopengraph/VLO8u7UXqclQ7byjfMEX0"


@pytest.mark.asyncio
async def test_fetch_helpers_for_public_post() -> None:
    async with AsyncMosirClient() as client:
        post = await client.get_post(post_id="VLO8u7UXqclQ7byjfMEX0")
        media = post["getPost"]["attachments"][0]["media"]

        media_bytes = await client.fetch_media(media)
        preview_bytes = await client.fetch_preview_image("post", "VLO8u7UXqclQ7byjfMEX0")

    assert len(media_bytes) > 0
    assert len(preview_bytes) > 0


@pytest.mark.asyncio
async def test_operation_normalizes_snake_case_variables() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["authorization"] = request.headers.get("authorization")
        payload = json.loads(request.content.decode())
        captured["payload"] = payload
        return httpx.Response(200, json={"data": {"ok": True}})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = AsyncMosirClient(token="secret", client=http_client)
        data = await client.operation("get_account_profile", account_id="abc", username="cat")

    assert data == {"ok": True}
    assert captured["authorization"] == "Bearer secret"
    assert captured["payload"] == {
        "query": OPERATION_REGISTRY["get_account_profile"].document,
        "variables": {"accountId": "abc", "username": "cat"},
        "operationName": "GetAccountProfile",
    }


@pytest.mark.asyncio
async def test_dynamic_method_uses_operation_registry() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        return httpx.Response(200, json={"data": {"echo": payload["operationName"]}})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = AsyncMosirClient(client=http_client)
        data = await client.get_notifications(limit=5)

    assert data == {"echo": "GetNotifications"}


def test_unknown_dynamic_method_raises_attribute_error() -> None:
    client = AsyncMosirClient()
    try:
        with pytest.raises(AttributeError):
            getattr(client, "does_not_exist")
    finally:
        import asyncio

        asyncio.run(client.aclose())


@pytest.mark.asyncio
async def test_operation_rejects_subscription_name() -> None:
    async with AsyncMosirClient() as client:
        with pytest.raises(ValueError, match="subscription"):
            await client.operation("post_created_by_author", author_id="abc")


@pytest.mark.asyncio
async def test_subscribe_operation_rejects_query_name() -> None:
    async with AsyncMosirClient() as client:
        with pytest.raises(ValueError, match="not a subscription"):
            client.subscribe_operation("get_post", post_id="abc")


def test_fetch_media_requires_available_file() -> None:
    client = AsyncMosirClient()
    try:
        with pytest.raises(ValueError, match="No media file"):
            import asyncio

            asyncio.run(client.fetch_media({}))
    finally:
        import asyncio

        asyncio.run(client.aclose())
