import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Union

import aiofiles

from .database import DataBase
from .transformation import transform


async def read_transform_ingest_all_files(assocs: dict, db: DataBase) -> None:
    base_path = Path(os.getenv("BASE_PATH", "/data"))
    coros = [
        read_transform_ingest_file(file, assocs, db)
        for day in base_path.iterdir()
        for file in day.iterdir()
    ]
    results = await asyncio.gather(*coros)
    print(f"Read {len(results)} files")


async def read_transform_ingest_file(path: Path, assocs: dict, db: DataBase) -> None:
    filename = "".join(path.name.split("_")[3:])
    assoc = assocs[filename]
    data = await read_file(path)

    transform_func = assoc["func"]
    key = assoc["key"]
    date = assemble_date_from_path(path)
    collection = assoc["collection"]

    transformed_data = transform(data, transform_func, key, date)
    await db.insert(collection, transformed_data)


async def read_file(path: Path) -> Union[dict, str]:
    try:
        async with aiofiles.open(path) as f:
            content = await f.read()
    except Exception as e:
        print(f"Could not read file: {path} with Exception {e}")
    if path.suffix == ".json":
        return json.loads(content)
    return content


def assemble_date_from_path(path: Path) -> datetime:
    ymd = path.parents[0].name.split("_")
    hm = path.name.split("_")[1:3]
    ymdhm = [int(i) for i in ymd + hm]
    year, month, day, hour, minute = ymdhm
    return datetime(year, month, day, hour, minute)
