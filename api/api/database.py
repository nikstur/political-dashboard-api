import os
from typing import Dict, List

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCursor,
    AsyncIOMotorDatabase,
)


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

    async def find(self, collection_name: str, *filters: Dict) -> List[Dict]:
        """Find data and clean it"""
        collection: AsyncIOMotorClient = self.db[collection_name]
        db_filter: Dict = self.combine_filters(*filters)
        cursor: AsyncIOMotorCursor = collection.find(db_filter)
        docs: List[Dict] = [self.clean_doc(doc) async for doc in cursor]
        return docs

    def combine_filters(self, *filters: Dict) -> Dict:
        base_filter = filters[0]
        for f in filters[1:]:
            if f:
                base_filter.update(f)
        return base_filter

    def clean_doc(self, doc: Dict) -> Dict:
        """Remove database ID and change date from datetime to date"""
        doc.pop("_id")
        doc["date"] = doc["date"].date()
        return doc

    def disconnect(self) -> None:
        self.client.close()


database = DataBase()
