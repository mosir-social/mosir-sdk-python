# mosir-sdk-python

Python SDK for the Mosir public GraphQL API.

## Status

Production-ready async client library.

Current focus:
- async transport with `httpx`
- dynamic snake_case wrappers resolved from `public.operations.graphql`
- SSE subscriptions with `httpx-sse`
- optional Bearer token auth
- shared public artifacts:
  - `public.graphqls`
  - `public.operations.graphql`

## Install

For package users:

```bash
pip install mosir-sdk-python
```

or:

```bash
uv add mosir-sdk-python
```

For local development in this repository:

```bash
uv sync
```

## Quick example

### Anonymous/public request

Only public data needs no token.

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        post = await client.get_post(post_id="VLO8u7UXqclQ7byjfMEX0")
        print(post["getPost"]["content"])


asyncio.run(main())
```

### Authenticated request

Use a token for authenticated operations such as notifications.

```python
import asyncio
import os

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient(token=os.getenv("MOSIR_API_TOKEN")) as client:
        notifications = await client.get_notifications(limit=20)
        print(notifications["getNotifications"])


asyncio.run(main())
```

## More examples

### Fetch media bytes from a `Media` result

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        post = await client.get_post(post_id="VLO8u7UXqclQ7byjfMEX0")
        media = post["getPost"]["attachments"][0]["media"]
        media_bytes = await client.fetch_media(media)
        print(len(media_bytes))


asyncio.run(main())
```

### Fetch preview image for a post, profile, or collection

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        print(client.get_preview_image_url("post", "VLO8u7UXqclQ7byjfMEX0"))
        preview_bytes = await client.fetch_preview_image("post", "VLO8u7UXqclQ7byjfMEX0")
        print(len(preview_bytes))


asyncio.run(main())
```

### SSE subscription example

Subscriptions let your app receive updates from Mosir in near real time without polling.
This SDK uses **SSE** (Server-Sent Events) for subscriptions.

A good example is a Discord bot:
- subscribe to `post_created_by_author(...)`
- when a creator publishes something new, turn it into a message
- send that message into a Discord channel

That way the bot reacts immediately instead of polling the API on a timer.
SSE works especially well for long-running workers, bots, and notification bridges that only need a one-way event stream from the server.
For public subscriptions like `post_created_by_author(...)`, a token is not required.

Note: each SSE connection lasts at most 1 hour. In practice, network conditions may cause it to end earlier.
If you build a bot, worker, or relay process, make sure you implement reconnect logic.

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        profile = await client.get_account_profile(username="leemiyinghao")
        author_id = profile["getAccountProfile"]["id"]

        async for event in client.post_created_by_author(
            author_id=author_id,
            post_type="POST",
        ):
            print(event["postCreatedByAuthor"]["id"])
            print(event["postCreatedByAuthor"]["content"])
            break


asyncio.run(main())
```

## Notes

- default endpoint: `https://beta.mosir.app/api/v1`
- `token` is optional for public data and required only for authenticated operations
- the same applies to subscriptions: public subscription data does not require a token
- snake_case methods are resolved dynamically from the operation registry, for example:
  - `get_post(...)`
  - `get_notifications(...)`
  - `post_created_by_author(...)`
- media helpers are available through:
  - `select_media_file(...)`
  - `await client.fetch_media(...)`
- preview image helpers are available through:
  - `get_preview_image_url(...)`
  - `await client.fetch_preview_image(...)`
- explicit operation access is also available:
  - `await client.operation("get_post", post_id="...")`
  - `client.subscribe_operation("post_created_by_author", author_id="...", post_type="POST")`
    - you can resolve `author_id` first with `get_account_profile(username="...")`
- raw GraphQL is still available through:
  - `await client.request(...)`
  - `client.subscribe(...)`

## Release / publish prep

Build and validate distributions before uploading to PyPI:

```bash
task build
task package-check
```

Typical upload flow:

```bash
uvx twine upload dist/*
```

## Tasks

```bash
task install
task codegen
task pyright
task test
task build
task package-check
task smoke
```
