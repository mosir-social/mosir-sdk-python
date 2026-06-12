# mosir-sdk-python

Python SDK for the Mosir public GraphQL API.

## What this SDK provides

- generated operation registry from `public.operations.graphql`
- dynamic snake_case operation methods (query, mutation, subscription)
- optional Bearer token auth
- default endpoint: `https://beta.mosir.app/api/v1`
- SSE subscription support out of the box
- raw GraphQL access for developers who want direct control

## Transport choice

This SDK uses:

- `httpx` for queries and mutations
- `httpx-sse` for subscriptions

This keeps the package small while still supporting the preferred subscription transport.
WebSocket support is intentionally not bundled. If you want WebSocket subscriptions, use your own GraphQL/WebSocket client.

## Install

```bash
pip install mosir-sdk-python
```

or:

```bash
uv add mosir-sdk-python
```

## Quick start

### Anonymous/public requests

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

### Authenticated requests

Use a token for authenticated operations such as notifications.

```python
import asyncio
import os

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient(token=os.getenv("MOSIR_API_TOKEN")) as client:
        notifications = await client.get_notifications(limit=20)
        print(notifications["getNotifications"]["edges"])


asyncio.run(main())
```

## Custom endpoint

```python
from mosir_sdk import AsyncMosirClient

client = AsyncMosirClient(
    token="YOUR_TOKEN",
    endpoint="https://example.com/api/v1",
)
```

## Common usage examples

### Get a post

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        post = await client.get_post(post_id="VLO8u7UXqclQ7byjfMEX0")
        print(post["getPost"]["author"]["username"])
        print(post["getPost"]["content"])


asyncio.run(main())
```

### Get replies under a post

Replies are exposed as nested GraphQL fields on `Post`, so this is a good case for direct GraphQL usage:

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        replies = await client.request(
            """
            query GetPostReplies($postId: ID!, $limit: Int) {
              getPost(postId: $postId) {
                id
                commentsRecent(limit: $limit) {
                  edges {
                    id
                    content
                    createdAt
                    author {
                      id
                      username
                      displayName
                    }
                  }
                  pageInfo {
                    endCursor
                    hasNextPage
                    totalCount
                  }
                }
              }
            }
            """,
            {
                "postId": "VLO8u7UXqclQ7byjfMEX0",
                "limit": 3,
            },
        )

        print(replies["getPost"]["commentsRecent"]["edges"])


asyncio.run(main())
```

### Get notifications

```python
import asyncio
import os

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient(token=os.getenv("MOSIR_API_TOKEN")) as client:
        notifications = await client.get_notifications(limit=20)
        print(notifications["getNotifications"]["edges"])


asyncio.run(main())
```

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
        preview_url = client.get_preview_image_url("post", "VLO8u7UXqclQ7byjfMEX0")
        print(preview_url)

        preview_bytes = await client.fetch_preview_image("post", "VLO8u7UXqclQ7byjfMEX0")
        print(len(preview_bytes))


asyncio.run(main())
```

## SSE subscriptions

Subscriptions let your app receive updates from Mosir in near real time without polling.
This SDK uses **SSE** (Server-Sent Events) for subscriptions by default.

A good example is a Discord bot:
- subscribe to `post_created_by_author`
- when a creator publishes something new, format it
- send a message into a Discord channel

That way the bot reacts as soon as something changes, instead of repeatedly calling the API every few seconds.
SSE is especially useful for backend workers, bots, notification relays, and other long-running processes that want a simple one-way stream of events from the server.
For public subscriptions like `post_created_by_author`, a token is not required.

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


asyncio.run(main())
```

You can also use the lower-level operation subscription API:

```python
stream = client.subscribe_operation(
    "post_created_by_author",
    author_id=author_id,
    post_type="POST",
)
```

## Raw GraphQL access

Authentication is optional. Pass `token` for authenticated operations, or omit it when accessing only public data.

### Operation usage

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        data = await client.operation("get_notifications", limit=20)
        print(data)


asyncio.run(main())
```

### Raw GraphQL string usage

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        replies = await client.request(
            """
            query GetPostReplies($postId: ID!, $limit: Int) {
              getPost(postId: $postId) {
                id
                commentsRecent(limit: $limit) {
                  edges {
                    id
                    content
                    createdAt
                    author {
                      username
                      displayName
                    }
                  }
                }
              }
            }
            """,
            {
                "postId": "VLO8u7UXqclQ7byjfMEX0",
                "limit": 3,
            },
        )

        print(replies)


asyncio.run(main())
```

## WebSocket usage

WebSocket transport is not bundled.
If you want it, use your own GraphQL WebSocket client against the same endpoint.

## Notes

- default endpoint: `https://beta.mosir.app/api/v1`
- `token` is optional for public data and required only for authenticated operations
- the same applies to subscriptions: public subscription data does not require a token
- snake_case methods are resolved dynamically from the operation registry
- media helpers are available through `select_media_file(...)` and `fetch_media(...)`
- preview image helpers are available through `get_preview_image_url(...)` and `fetch_preview_image(...)`
- subscriptions use SSE in this SDK
- direct GraphQL usage is supported through `operation(...)`, `request(...)`, `subscribe_operation(...)`, and `subscribe(...)`

## Development

### Install

```bash
task install
```

### Generate code

```bash
task codegen
```

### Typecheck

```bash
task pyright
```

### Build

```bash
task build
```

### Full check

```bash
task check
```

## Repo artifacts

- `public.graphqls` — copied public schema artifact
- `public.operations.graphql` — copied curated operation document
- `src/mosir_sdk/_operations.py` — generated operation registry
- `src/mosir_sdk/client.py` — async client and helpers

## License

This project is licensed under the GNU Lesser General Public License v3.0 (LGPL-3.0).
See [`LICENSE`](./LICENSE) for details.
