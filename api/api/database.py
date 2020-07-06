import os
from typing import Dict, List

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class DataBase:
    def __init__(self) -> None:
        self.hostname: str = os.getenv("DB_HOSTNAME", "db")

    def connect(self) -> None:
        self._get_client()
        self._get_db()

    def _get_client(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(host=self.hostname)

    def _get_db(self) -> None:
        self.db: AsyncIOMotorDatabase = self.client["database"]

    async def find_twitter(
        self, base_filter: Dict, additional_filters: List[Dict]
    ) -> List[Dict]:
        return await self._find_and_clean("twitter", base_filter, additional_filters)

    async def find_facebook(
        self, base_filter: Dict, additional_filters: List[Dict]
    ) -> List[Dict]:
        return await self._find_and_clean("facebook", base_filter, additional_filters)

    async def find_media(
        self, base_filter: Dict, additional_filters: List[Dict]
    ) -> List[Dict]:
        return await self._find_and_clean("media", base_filter, additional_filters)

    def _add_filter(self, base_filter: Dict, additional_filters: List[Dict]) -> Dict:
        for f in additional_filters:
            if f:
                base_filter.update(f)
        return base_filter

    async def _find_and_clean(
        self, collection_name: str, base_filter: Dict, additional_filters: List[Dict]
    ) -> List[Dict]:
        """Find data, remove datbase ID, and change date from datetime to date"""
        collection = self.db[collection_name]
        db_filter = self._add_filter(base_filter, additional_filters)

        cursor = collection.find(db_filter)
        docs = [self.clean_doc(doc) async for doc in cursor]
        return docs

    def clean_doc(self, doc: Dict) -> Dict:
        doc.pop("_id")
        doc["date"] = doc["date"].date()
        return doc

    def disconnect(self) -> None:
        self.client.close()


database = DataBase()


def get_database() -> DataBase:
    return database
