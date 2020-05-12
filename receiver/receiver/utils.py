import json
import asyncio
from pathlib import Path

import aiohttp


def load_data_into_db(directory, collection):
    data_list = []
    for file in directory.iterdir():
        if file.suffix == ".json":
            with open(file) as f:
                data = json.load(f)
            data_list.append(data)
    collection.insert_many(data_list)


async def fetch(session, url):
    async with session.get(url) as response:
        data = await response.json()
    return data


async def fetch_multiple(session, urls, fetch_function):
    results = await asyncio.gather(
        *[fetch_function(session, url) for url in urls], return_exceptions=True
    )
    return [result for result in results if not isinstance(result, Exception)]
