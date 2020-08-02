import asyncio
from functools import partial
from typing import Dict

import aiohttp
import typer

from . import database
from .fetch import endpoints, fetch_all_endpoints

app = typer.Typer()


@app.command()
def initial() -> None:
    asyncio.run(initial_setup())


@app.command()
def continual() -> None:
    asyncio.run(download_and_insert_from_endpoints())


async def initial_setup() -> None:
    await insert_initial_api_key()
    await read_and_insert_from_files()
    await download_and_insert_from_endpoints()


async def insert_initial_api_key():
    db = database.setup("administration")
    initial_doc: Dict = {
        "identifier": 1,
        "hash": "$2b$12$7pmPKz6uqV5DIFR7b7R0IuWXND0WdPQDM/1neOf.oTJXclqPd.ReW",
        "can_create_token": True,
        "created_by": 0,
    }
    db.api_keys.insert_one(initial_doc)


async def download_and_insert_from_endpoints() -> None:
    db = database.setup("content")

    async with aiohttp.ClientSession(headers={"Connection": "keep-alive"}) as session:
        fetch_endpoints = partial(fetch_all_endpoints, session=session)
        facebook_data = await fetch_endpoints(endpoints.facebook)
        media_data = await fetch_endpoints(endpoints.media)
        twitter_data = await fetch_endpoints(endpoints.twitter)

    db.facebook.insert_many(facebook_data)
    db.media.insert_many(media_data)
    db.twitter.insert_many(twitter_data)


async def read_and_insert_from_files() -> None:
    pass


if __name__ == "__main__":
    app()
