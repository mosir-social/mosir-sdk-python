from __future__ import annotations

import asyncio

from mosir_sdk import AsyncMosirClient

POST_ID = "VLO8u7UXqclQ7byjfMEX0"


async def main() -> None:
    async with AsyncMosirClient() as client:
        data = await client.get_post(post_id=POST_ID)
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
