import asyncio
from functools import partial

import aiohttp

from . import database
from .fetch import endpoints, fetch_all_endpoints


async def main() -> None:
    twitter_col, facebook_col, media_col = database.setup(drop_all=True)

    async with aiohttp.ClientSession(headers={"Connection": "keep-alive"}) as session:
        fetch_endpoints = partial(fetch_all_endpoints, session=session)
        facebook_data = await fetch_endpoints(endpoints.facebook)
        media_data = await fetch_endpoints(endpoints.media)
        twitter_data = await fetch_endpoints(endpoints.twitter)

    facebook_col.insert_many(facebook_data)
    media_col.insert_many(media_data)
    twitter_col.insert_many(twitter_data)


if __name__ == "__main__":
    asyncio.run(main())
