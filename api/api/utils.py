async def get_cleaned_docs(collection, filter=None):
    cursor = collection.find(filter)
    docs = []
    async for doc in cursor:
        doc.pop("_id")
        docs.append(doc)
    return docs
