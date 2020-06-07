import os
from typing import Dict, List

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)


class DataBase:
    def __init__(self) -> None:
        self.hostname: str = os.getenv("DB_HOSTNAME", "db")

    def connect(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(host=self.hostname)
        self._get_db()

    def disconnect(self) -> None:
        self.client.close()

    def drop_all(self) -> None:
        self.client.drop_database("database")

    def _get_db(self) -> None:
        self.db: AsyncIOMotorDatabase = self.client["database"]

    def _get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self.db[collection_name]

    async def _find_and_clean(
        self, collection: AsyncIOMotorCollection, filter: Dict = None
    ) -> List[Dict]:
        """Find data and remove datbase ID"""
        cursor = collection.find(filter)
        docs = []
        async for doc in cursor:
            doc.pop("_id")
            docs.append(doc)
        return docs

    async def find_twitter(self, filter: Dict = None) -> List[Dict]:
        return await self._find_and_clean(
            self._get_collection("twitter"), filter=filter
        )

    async def find_facebook(self, filter: Dict = None) -> List[Dict]:
        return await self._find_and_clean(
            self._get_collection("facebook"), filter=filter
        )

    async def find_media(self, filter: Dict = None) -> List[Dict]:
        return await self._find_and_clean(self._get_collection("media"), filter=filter)


database = DataBase()


def get_database() -> DataBase:
    return database
