def get_cleaned_docs(collection, filter=None):
    cursor = collection.find(filter)
    docs = []
    for doc in cursor:
        doc.pop("_id")
        docs.append(doc)
    return docs
