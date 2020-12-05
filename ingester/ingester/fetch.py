import asyncio
from typing import List, Union

from aiohttp import ClientSession

from .transformation import transform


async def fetch_and_transform_multiple_endpoints(
    associations: List[dict], session: ClientSession
) -> List[dict]:
    coros = [fetch_and_transform_single_endpoint(session, a) for a in associations]
    data = await asyncio.gather(*coros)
    return data


async def fetch_and_transform_single_endpoint(
    session: ClientSession, association: dict
) -> dict:
    base_url = "https://political-dashboard.com/json_files/"
    url = base_url + association["url"]
    data_type = association["type"]
    key = association["key"]
    transform_func = association["func"]

    data = await fetch_data(session, url, data_type)
    print("Fetched:", url)
    transformed_data = transform(data, transform_func, key)
    return transformed_data


async def fetch_data(
    session: ClientSession, url: str, data_type: str
) -> Union[dict, str]:
    async with session.get(url) as response:
        if data_type == "js":
            byte_data: bytes = await response.read()
            data = byte_data.decode("utf-8")
        elif data_type == "json":
            data = await response.json()
    return data
