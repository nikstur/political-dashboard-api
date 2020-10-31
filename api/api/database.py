import os
from typing import Dict, List

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorCursor,
    AsyncIOMotorDatabase,
)


class DataBaseConnection:
    def connect(self) -> None:
        hostname = os.getenv("DB_HOSTNAME", "db")
        self.client = AsyncIOMotorClient(host=hostname)
        self.db = DataBase(self.client)
        print("Connected to database")

    def disconnect(self) -> None:
        self.client.close()
        print("Disconnected from database")


class DataBase:
    def __init__(self, client: AsyncIOMotorClient) -> None:
        self.client: AsyncIOMotorClient = client
        self.db: AsyncIOMotorDatabase = self.client["database"]

    async def find(self, collection_name: str, *filters: Dict) -> List[Dict]:
        """Find data and clean it"""
        collection: AsyncIOMotorCollection = self.db[collection_name]
        db_filter: Dict = self._combine_filters(*filters)
        cursor: AsyncIOMotorCursor = collection.find(db_filter)
        docs: List[Dict] = [self._clean_doc(doc) async for doc in cursor]
        return docs

    def _combine_filters(self, *filters: Dict) -> Dict:
        """Combine multiple filters into one"""
        base_filter = filters[0]
        for f in filters[1:]:
            if f:
                base_filter.update(f)
        return base_filter

    def _clean_doc(self, doc: Dict) -> Dict:
        """Remove database ID and change date from datetime to date"""
        doc.pop("_id")
        doc["date"] = doc["date"].date()
        return doc


database_connection = DataBaseConnection()
