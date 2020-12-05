import asyncio
from functools import partial

import aiohttp
import typer

from .database import database_connection
from .fetch import fetch_and_transform_multiple_endpoints
from .transformation import associations

app = typer.Typer()


@app.command()
def initial() -> None:
    with database_connection() as db_conn:
        asyncio.run(initial_setup(db_conn))


@app.command()
def continual() -> None:
    with database_connection() as db_conn:
        asyncio.run(download_and_insert_from_endpoints(db_conn))


async def initial_setup(db_conn) -> None:
    await read_and_insert_from_files(db_conn)
    await download_and_insert_from_endpoints(db_conn)


async def read_and_insert_from_files(db_conn) -> None:
    pass


async def download_and_insert_from_endpoints(db_conn) -> None:
    async with aiohttp.ClientSession(headers={"Connection": "keep-alive"}) as session:
        fetch = partial(fetch_and_transform_multiple_endpoints, session=session)
        facebook_data = await fetch(associations.facebook)
        media_data = await fetch(associations.media)
        twitter_data = await fetch(associations.twitter)

    # The db object is necessary because MongoDB itself has the concept of a database
    # while db_conn is the connection to MonogDB as a DBMS
    db_conn.db.facebook.insert_many(facebook_data)
    db_conn.db.media.insert_many(media_data)
    db_conn.db.twitter.insert_many(twitter_data)


if __name__ == "__main__":
    app()
