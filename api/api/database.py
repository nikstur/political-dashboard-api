import os
from typing import Dict, List

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCursor,
    AsyncIOMotorDatabase,
)


class DataBase:
    db_name: str = ""

    def __init__(self, client: AsyncIOMotorClient) -> None:
        self.client: AsyncIOMotorClient = client

    def connect(self) -> None:
        self.db: AsyncIOMotorDatabase = self.client[self.db_name]
        print(f"Connected to database: {self.db_name}")

    def disconnect(self) -> None:
        self.client.close()
        print(f"Disconnected from database: {self.db_name}")


class DBContent(DataBase):
    db_name: str = "content"

    async def find(self, collection_name: str, *filters: Dict) -> List[Dict]:
        """Find data and clean it"""
        collection: AsyncIOMotorClient = self.db[collection_name]
        db_filter: Dict = self.combine_filters(*filters)
        cursor: AsyncIOMotorCursor = collection.find(db_filter)
        docs: List[Dict] = [self.clean_doc(doc) async for doc in cursor]
        return docs

    def combine_filters(self, *filters: Dict) -> Dict:
        """Combine multiple filters into one"""
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


class DBAdmin(DataBase):
    db_name: str = "administration"

    async def find(self, collection_name: str, identifier: int) -> Dict:
        collection: AsyncIOMotorClient = self.db[collection_name]
        doc: Dict = await collection.find_one({"identifier": identifier})
        return doc

    async def count(self, collection_name: str) -> int:
        collection: AsyncIOMotorClient = self.db[collection_name]
        doc_count: int = await collection.count_documents({})
        return doc_count

    async def insert(self, collection_name: str, doc: Dict) -> None:
        collection: AsyncIOMotorClient = self.db[collection_name]
        await collection.insert_one(doc)


hostname: str = os.getenv("DB_HOSTNAME", "db")
client: AsyncIOMotorClient = AsyncIOMotorClient(host=hostname)
db_content: DBContent = DBContent(client)
db_admin: DBAdmin = DBAdmin(client)
