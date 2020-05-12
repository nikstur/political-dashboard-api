import asyncio
import json
from pathlib import Path
from pprint import pprint
from urllib.parse import urlparse

import aiohttp
from pymongo import MongoClient

from receiver import twitter, utils

# client = MongoClient(host="172.17.0.2")
client = MongoClient(host="db")
db = client["database"]
db.drop_collection("twitter")
twitter_col = db["twitter"]


async def main():
    twitter_results = await twitter.get_twitter()
    twitter_col.insert_many(twitter_results)


if __name__ == "__main__":
    asyncio.run(main())
