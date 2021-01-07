import asyncio

import typer

from .fetch import fetch_transform_ingest_all
from .read import read_transform_ingest_all
from .transformation import associations

app = typer.Typer()


@app.command()
def initial() -> None:
    asyncio.run(read_transform_ingest_all(associations))
    asyncio.run(fetch_transform_ingest_all(associations))


@app.command()
def continual() -> None:
    asyncio.run(fetch_transform_ingest_all(associations))


if __name__ == "__main__":
    app()
