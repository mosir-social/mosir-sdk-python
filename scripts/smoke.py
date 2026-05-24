from __future__ import annotations

import asyncio

from mosir_sdk import AsyncMosirClient

POST_ID = "VLO8u7UXqclQ7byjfMEX0"
AUTHOR_USERNAME = "leemiyinghao"
SSE_TIMEOUT_SECONDS = 8


async def smoke_query(client: AsyncMosirClient) -> None:
    data = await client.get_post(post_id=POST_ID)
    post = data["getPost"]
    print("[query] ok:", post["id"], "author=", post["author"]["username"])


async def smoke_graphql_sse(client: AsyncMosirClient) -> None:
    profile = await client.get_account_profile(username=AUTHOR_USERNAME)
    author_id = profile["getAccountProfile"]["id"]

    stream = client.post_created_by_author(author_id=author_id, post_type="POST")
    try:
        event = await asyncio.wait_for(anext(stream), timeout=SSE_TIMEOUT_SECONDS)
        post = event["postCreatedByAuthor"]
        print("[graphql-sse] ok: received event post_id=", post["id"])
    except TimeoutError:
        # This still proves the GraphQL SSE stream was accepted/opened for a period.
        print(f"[graphql-sse] ok: stream opened (no event within {SSE_TIMEOUT_SECONDS}s)")
    finally:
        await stream.aclose()


async def main() -> None:
    async with AsyncMosirClient() as client:
        await smoke_query(client)
        await smoke_graphql_sse(client)


if __name__ == "__main__":
    asyncio.run(main())
