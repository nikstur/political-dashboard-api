import asyncio
import os
from datetime import datetime
from typing import Union

from aiohttp import ClientSession

from .database import DataBase, database_connection
from .transformation import transform


async def fetch_transform_ingest_all_endpoints(assocs: dict) -> None:
    with database_connection() as db:
        async with ClientSession(headers={"Connection": "keep-alive"}) as session:
            coros = [
                fetch_transform_ingest_endpoint(session, assoc, db)
                for _, assoc in assocs.items()
            ]
            results = await asyncio.gather(*coros)
    print(f"Fetched {len(results)} endpoints")


async def fetch_transform_ingest_endpoint(
    session: ClientSession, assoc: dict, db: DataBase
) -> None:
    base_url = os.getenv("BASE_URL", "https://political-dashboard.com/json_files/")
    url = base_url + assoc["path"]
    data = await fetch_endpoint(session, url)

    transform_func = assoc["func"]
    key = assoc["key"]
    date = datetime.utcnow()
    collection = assoc["collection"]

    transformed_data = transform(data, transform_func, key, date)
    await db.insert(collection, transformed_data)


async def fetch_endpoint(session: ClientSession, url: str) -> Union[dict, str]:
    async with session.get(url) as response:
        if response.status == 200:
            if response.headers["Content-Type"] == "application/json":
                return await response.json()
            else:
                return await response.text(encoding="utf-8")
        else:
            raise Exception(f"Could not get: {url}")
