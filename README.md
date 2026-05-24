# mosir-sdk-python

Python SDK for the Mosir public GraphQL API.

## Status

Early scaffold, but already usable.

Current focus:
- async transport with `httpx`
- dynamic snake_case wrappers resolved from `public.operations.graphql`
- SSE subscriptions with `httpx-sse`
- optional Bearer token auth
- shared public artifacts:
  - `public.graphqls`
  - `public.operations.graphql`

## Install

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

```python
import asyncio
import os

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient(token=os.getenv("MOSIR_API_TOKEN")) as client:
        async for event in client.post_updated(post_id="VLO8u7UXqclQ7byjfMEX0"):
            print(event["postUpdated"]["id"])
            break


asyncio.run(main())
```

## Notes

- default endpoint: `https://beta.mosir.app/api/v1`
- `token` is optional for public data and required only for authenticated operations
- snake_case methods are resolved dynamically from the operation registry, for example:
  - `get_post(...)`
  - `get_notifications(...)`
  - `post_updated(...)`
- media helpers are available through:
  - `select_media_file(...)`
  - `await client.fetch_media(...)`
- preview image helpers are available through:
  - `get_preview_image_url(...)`
  - `await client.fetch_preview_image(...)`
- explicit operation access is also available:
  - `await client.operation("get_post", post_id="...")`
  - `client.subscribe_operation("post_updated", post_id="...")`
- raw GraphQL is still available through:
  - `await client.request(...)`
  - `client.subscribe(...)`

## Tasks

```bash
task install
task codegen
task pyright
task test
task smoke
```
