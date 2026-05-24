# mosir-sdk-python

Python SDK for the Mosir public GraphQL API.

## Status

Early scaffold.

Current focus:
- async transport with `httpx`
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
        post = await client.request(
            """
            query GetPost($postId: ID!) {
              getPost(postId: $postId) {
                id
                content
                author {
                  username
                }
              }
            }
            """,
            {"postId": "VLO8u7UXqclQ7byjfMEX0"},
        )
        print(post)


asyncio.run(main())
```

## Tasks

```bash
task install
task pyright
task smoke
```
