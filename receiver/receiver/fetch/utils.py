import asyncio
import json
from pathlib import Path
from typing import Callable, Dict, List
from urllib.parse import urlparse

import aiohttp
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorCollection


def load_data_into_db(directory: Path, collection: AsyncIOMotorCollection) -> None:
    data_list = []
    for file in directory.iterdir():
        if file.suffix == ".json":
            with open(file) as f:
                data = json.load(f)
            data_list.append(data)
    collection.insert_many(data_list)


async def get_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    filename = parsed_url.path.split("/")[-1].split(".")[0]
    return filename


async def get_data_from_endpoints(
    session: ClientSession,
    endpoints: List[str],
    base_url: str,
    fetch_function: Callable,
) -> List[Dict]:
    urls = [base_url + endpoint for endpoint in endpoints]
    data = await fetch_multiple(session, urls, fetch_function)
    return data


async def fetch_multiple(
    session: ClientSession, urls: List[str], fetch_function: Callable
) -> List[Dict]:
    results = await asyncio.gather(*[fetch_function(session, url) for url in urls])
    return results
