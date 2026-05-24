# mosir-sdk-python

Python SDK for the Mosir public GraphQL API.

## Status

Early scaffold, but already usable.

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

### Anonymous/public request

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

## Notes

- default endpoint: `https://beta.mosir.app/api/v1`
- `token` is optional
- generated methods are snake_case, for example:
  - `get_post(...)`
  - `get_notifications(...)`
  - `post_updated(...)`
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
