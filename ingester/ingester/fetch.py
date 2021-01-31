import asyncio
import os
from datetime import datetime
from typing import Union

from aiohttp import ClientSession

from .database import DataBase, database_connection
from .transformation import transform


async def fetch_transform_ingest_all(assocs: dict) -> None:
    with database_connection() as db:
        async with ClientSession(headers={"Connection": "keep-alive"}) as session:
            coros = [
                fetch_transform_ingest(session, assoc, db)
                for _, assoc in assocs.items()
            ]
            results = await asyncio.gather(*coros, return_exceptions=True)
    successes = [i for i in results if not isinstance(i, Exception)]
    failures = [i for i in results if isinstance(i, Exception)]
    print(f"Successfully fetched {len(successes)} file(s)")
    print(f"Failed to fetch {len(failures)} file(s)")
    for i, f in enumerate(failures):
        print(f"Failure {i+1}: {f}")


async def fetch_transform_ingest(
    session: ClientSession, assoc: dict, db: DataBase
) -> None:
    base_url = os.getenv("BASE_URL", "https://political-dashboard.com/json_files/")
    url = base_url + assoc["path"]
    try:
        data = await fetch(session, url)
    except Exception as e:
        raise Exception(f"Could not fetch file: {url} with Exception {e}")
    else:
        transform_func = assoc["func"]
        key = assoc["key"]
        date = datetime.utcnow()
        collection = assoc["collection"]
        party = assoc.get("party")
        try:
            transformed_data = transform(data, transform_func, key, date, party)
        except Exception as e:
            raise Exception(f"Failed to transform data from {url} with Exception {e}")
        else:
            await db.insert(collection, transformed_data)


async def fetch(session: ClientSession, url: str) -> Union[dict, str]:
    async with session.get(url) as response:
        if response.status == 200:
            if response.headers["Content-Type"] == "application/json":
                return await response.json()
            else:
                return await response.text(encoding="utf-8")
        else:
            raise Exception(f"Could not get: {url}")
