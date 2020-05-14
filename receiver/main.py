import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
import aiohttp

from receiver import twitter, facebook, media

client = AsyncIOMotorClient(host="172.17.0.2")
# client = AsyncIOMotorClient(host="db")
db = client["database"]

db.drop_collection("twitter")
twitter_col = db["twitter"]

db.drop_collection("facebook")
facebook_col = db["facebook"]

db.drop_collection("media")
media_col = db["media"]


async def get_and_store(session, collection, module):
    results = await module.get_data(session)
    await collection.insert_many(results)


async def main():
    collections = [(twitter, twitter_col), (facebook, facebook_col), (media, media_col)]
    async with aiohttp.ClientSession() as session:
        for module, collection in collections:
            asyncio.create_task(get_and_store(session, collection, module))


if __name__ == "__main__":
    asyncio.run(main())
