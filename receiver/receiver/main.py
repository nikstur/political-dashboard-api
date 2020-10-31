import asyncio
from functools import partial

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
    await read_and_insert_from_files()
    await download_and_insert_from_endpoints()


async def read_and_insert_from_files() -> None:
    pass


async def download_and_insert_from_endpoints() -> None:
    db_content = database.setup("database")

    async with aiohttp.ClientSession(headers={"Connection": "keep-alive"}) as session:
        fetch_endpoints = partial(fetch_all_endpoints, session=session)
        facebook_data = await fetch_endpoints(endpoints.facebook)
        media_data = await fetch_endpoints(endpoints.media)
        twitter_data = await fetch_endpoints(endpoints.twitter)

    db_content.facebook.insert_many(facebook_data)
    db_content.media.insert_many(media_data)
    db_content.twitter.insert_many(twitter_data)


if __name__ == "__main__":
    app()
