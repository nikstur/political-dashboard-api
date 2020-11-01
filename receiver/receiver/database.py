import os
from contextlib import contextmanager

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@contextmanager
def database_connection():
    try:
        database_connection = DataBaseConnection()
        database_connection.connect()
        yield database_connection
    finally:
        database_connection.disconnect()


class DataBaseConnection:
    def connect(self):
        hostname = os.getenv("DB_HOSTNAME", "db")
        self.client = AsyncIOMotorClient(host=hostname)
        self.db: AsyncIOMotorDatabase = self.client["database"]
        print("Connected to database")

    def disconnect(self):
        self.client.close()
        print("Disconnected from database")
