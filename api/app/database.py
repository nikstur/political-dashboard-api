import os

from motor.motor_asyncio import AsyncIOMotorClient

db_hostname = os.getenv("DB_HOSTNAME")


def create_find_and_clean(collection):
    async def find_and_clean(filter=None):
        cursor = collection.find(filter)
        docs = []
        async for doc in cursor:
            doc.pop("_id")
            docs.append(doc)
        return docs

    return find_and_clean


def get_collection(collection_name):
    db = setup()
    return db[collection_name]


def setup(drop_all=False):
    client = AsyncIOMotorClient(host=db_hostname)
    if drop_all:
        client.drop_database("database")
    db = client["database"]
    return db
