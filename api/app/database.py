import os
from typing import Callable

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

db_hostname = os.getenv("DB_HOSTNAME")


def create_find_and_clean(collection: AsyncIOMotorCollection) -> Callable:
    async def find_and_clean(filter=None):
        cursor = collection.find(filter)
        docs = []
        async for doc in cursor:
            doc.pop("_id")
            docs.append(doc)
        return docs

    return find_and_clean


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    db = setup()
    return db[collection_name]


def setup(drop_all: bool = False) -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(host=db_hostname)
    if drop_all:
        client.drop_database("database")
    db = client["database"]
    return db
