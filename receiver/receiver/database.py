import os

from pymongo import MongoClient
from pymongo.database import Database

db_hostname = os.getenv("DB_HOSTNAME", "db")
client: MongoClient = MongoClient(host=db_hostname)
print(f"Connected to database: {db_hostname}")


def setup(db_name) -> Database:
    client.drop_database(db_name)
    db = client[db_name]
    return db
