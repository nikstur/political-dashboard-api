import os

from motor.motor_asyncio import AsyncIOMotorClient

db_hostname = os.getenv("DB_HOSTNAME", "db")
print(f"{db_hostname}")


def setup(drop_all: bool = False):
    client = AsyncIOMotorClient(host=db_hostname)
    db = client["database"]
    if drop_all:
        client.drop_database("database")
    twitter_col = db["twitter"]
    facebook_col = db["facebook"]
    media_col = db["media"]
    return twitter_col, facebook_col, media_col
