# mosir-sdk-python

Python SDK for the Mosir public GraphQL API.

## Status

Early scaffold.

Current focus:
- async transport with `httpx`
- generated snake_case wrappers from `public.operations.graphql`
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

```python
import asyncio

from mosir_sdk import AsyncMosirClient


async def main() -> None:
    async with AsyncMosirClient() as client:
        post = await client.get_post(post_id="VLO8u7UXqclQ7byjfMEX0")
        print(post["getPost"])

        notifications = await client.get_notifications(limit=20)
        print(notifications["getNotifications"])


asyncio.run(main())
```

## Tasks

```bash
task install
task codegen
task pyright
task test
task smoke
```
