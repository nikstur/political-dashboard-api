import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import aiohttp

from receiver import twitter, facebook, media

client = AsyncIOMotorClient(host="172.17.0.2")
# client = AsyncIOMotorClient(host="db")
# client = MongoClient(host="172.17.0.2")
db = client["database"]

db.drop_collection("twitter")
twitter_col = db["twitter"]

db.drop_collection("facebook")
facebook_col = db["facebook"]

db.drop_collection("media")
media_col = db["media"]


async def main():
    async with aiohttp.ClientSession() as session:
        twitter_results = await twitter.get_data(session)
        facebook_results = await facebook.get_data(session)
        media_results = await media.get_data(session)

    twitter_col.insert_many(twitter_results)
    facebook_col.insert_many(facebook_results)
    media_col.insert_many(media_results)


if __name__ == "__main__":
    asyncio.run(main())
