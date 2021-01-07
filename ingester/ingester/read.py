import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Union

import aiofiles

from .database import DataBase, database_connection
from .transformation import transform


async def read_transform_ingest_all(assocs: dict) -> None:
    base_path = Path(os.getenv("BASE_PATH", "/data"))
    try:
        with database_connection() as db:
            coros = [
                read_transform_ingest(file, assocs, db)
                for day in base_path.iterdir()
                for file in day.iterdir()
            ]
    except FileNotFoundError as e:
        print(f"Could not open directory: {base_path} with Exception {e}")
    else:
        results = await asyncio.gather(*coros, return_exceptions=True)
        successes = [i for i in results if not isinstance(i, Exception)]
        failures = [i for i in results if isinstance(i, Exception)]
        print(f"Successfully read {len(successes)} file(s)")
        print(f"Failed to read {len(failures)} file(s)")
        for i, f in enumerate(failures):
            print(f"Failure {i+1}: {f}")


async def read_transform_ingest(path: Path, assocs: dict, db: DataBase) -> None:
    try:
        data = await read(path)
    except Exception as e:
        raise Exception(f"Could not read file: {path} with Exception {e}")
    else:
        filename = "_".join(path.name.split("_")[3:])
        assoc = assocs[filename]
        transform_func = assoc["func"]
        key = assoc["key"]
        date = assemble_date_from_path(path)
        collection = assoc["collection"]
        try:
            transformed_data = transform(data, transform_func, key, date)
        except Exception as e:
            raise Exception(f"Failed to transform data from {path} with Exception {e}")
        else:
            await db.insert(collection, transformed_data)


async def read(path: Path) -> Union[dict, str]:
    async with aiofiles.open(path) as f:
        content = await f.read()
    if path.suffix == ".json":
        return json.loads(content)
    return content


def assemble_date_from_path(path: Path) -> datetime:
    ymd = path.parents[0].name.split("_")
    hm = path.name.split("_")[1:3]
    ymdhm = [int(i) for i in ymd + hm]
    year, month, day, hour, minute = ymdhm
    return datetime(year, month, day, hour, minute)
