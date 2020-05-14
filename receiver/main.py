import asyncio

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

from receiver import facebook, media, twitter


def setup_db(host_name, drop_all=False):
    client = AsyncIOMotorClient(host=host_name)
    db = client["database"]
    if drop_all:
        client.drop_database("database")
    twitter_col = db["twitter"]
    facebook_col = db["facebook"]
    media_col = db["media"]
    return twitter_col, facebook_col, media_col


async def main():
    twitter_col, facebook_col, media_col = setup_db("172.17.0.2", drop_all=True)

    async with aiohttp.ClientSession() as session:
        twitter_results = await twitter.get_data(session)
        facebook_results = await facebook.get_data(session)
        media_results = await media.get_data(session)

    twitter_col.insert_many(twitter_results)
    facebook_col.insert_many(facebook_results)
    media_col.insert_many(media_results)


if __name__ == "__main__":
    asyncio.run(main())
