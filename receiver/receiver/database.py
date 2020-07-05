import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

db_hostname = os.getenv("DB_HOSTNAME", "db")
print(f"{db_hostname=}")


def setup(drop_all: bool = False) -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(host=db_hostname)
    db = client["database"]
    if drop_all:
        client.drop_database("database")
    return db
