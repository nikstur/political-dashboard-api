import asyncio

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

from . import database, fetch


async def main() -> None:
    twitter_col, facebook_col, media_col = database.setup(drop_all=True)

    async with aiohttp.ClientSession() as session:
        twitter_results = await fetch.twitter(session)
        facebook_results = await fetch.facebook(session)
        media_results = await fetch.media(session)

    twitter_col.insert_many(twitter_results)
    facebook_col.insert_many(facebook_results)
    media_col.insert_many(media_results)


if __name__ == "__main__":
    asyncio.run(main())
