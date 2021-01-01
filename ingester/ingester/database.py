import os
from contextlib import contextmanager

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@contextmanager
def database_connection():
    try:
        db = DataBase()
        db.connect()
        yield db
    finally:
        db.disconnect()


class DataBase:
    def connect(self):
        hostname = os.getenv("DB_HOSTNAME", "db")
        self.client = AsyncIOMotorClient(host=hostname)
        self.db: AsyncIOMotorDatabase = self.client["database"]
        print("Connected to database")

    def disconnect(self):
        self.client.close()
        print("Disconnected from database")

    async def insert(self, collection: str, doc: dict):
        await self.db[collection].insert_one(doc)
