import asyncio
from typing import Dict, List, Union

from aiohttp import ClientSession

from .endpoints import base_url
from .preprocessing import transform


async def fetch_all_endpoints(
    endpoints: List[Dict], session: ClientSession
) -> List[Dict]:
    for endpoint in endpoints:
        endpoint["url"] = base_url + endpoint["url"]

    fetch_coros = [fetch_single_endpoint(session, e) for e in endpoints]
    data = await asyncio.gather(*fetch_coros)

    return data


async def fetch_single_endpoint(session: ClientSession, endpoint: Dict) -> Dict:
    url = endpoint["url"]
    data_type = endpoint["type"]
    key = endpoint["key"]
    transform_func = endpoint["func"]

    data = await fetch_data(session, url, data_type)
    print("Fetched:", url)
    transformed_data = transform(data, transform_func, key)

    if endpoint.get("party", None):
        endpoint["party"] = endpoint["party"]

    return transformed_data


async def fetch_data(
    session: ClientSession, url: str, data_type: str
) -> Union[Dict, str]:
    async with session.get(url) as response:
        if data_type == "js":
            byte_data: bytes = await response.read()
            data: Union[str, Dict] = byte_data.decode("utf-8")
        elif data_type == "json":
            data = await response.json()
    return data