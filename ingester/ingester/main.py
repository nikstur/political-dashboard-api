import asyncio

import typer

from .fetch import fetch_transform_ingest_all_endpoints
from .read import read_transform_ingest_all_files
from .transformation import associations

app = typer.Typer()


@app.command()
def initial() -> None:
    # asyncio.run(read_transform_ingest_all_files(associations))
    asyncio.run(fetch_transform_ingest_all_endpoints(associations))


@app.command()
def continual() -> None:
    asyncio.run(fetch_transform_ingest_all_endpoints(associations))


if __name__ == "__main__":
    app()
