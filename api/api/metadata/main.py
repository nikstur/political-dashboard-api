from importlib.resources import read_text


def load_desc(filename: str) -> str:
    return read_text(__package__, filename)


openapi_tags = [
    {
        "name": "Twitter",
        "description": load_desc("description_twitter.md"),
    },
    {
        "name": "Media",
        "description": load_desc("description_media.md"),
    },
    {
        "name": "Facebook",
        "description": load_desc("description_facebook.md"),
    },
]
