import asyncio
import json
from pathlib import Path
from pprint import pprint
from urllib.parse import urlparse

import aiohttp
from pymongo import MongoClient

from receiver import twitter, facebook, utils

client = MongoClient(host="172.17.0.2")
# client = MongoClient(host="db")
db = client["database"]
db.drop_collection("twitter")
twitter_col = db["twitter"]
db.drop_collection("facebook")
facebook_col = db["facebook"]


async def main():
    twitter_results = await twitter.get_data()
    twitter_col.insert_many(twitter_results)

    facebook_results = await facebook.get_data()
    facebook_col.insert_many(facebook_results)


if __name__ == "__main__":
    asyncio.run(main())
