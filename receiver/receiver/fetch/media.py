from typing import Dict, List

from aiohttp import ClientSession

from . import utils
from .preprocess import media as preprocess


async def media(session: ClientSession) -> List[Dict]:
    endpoints = [
        # "topics_news.json",
        "news_party_attention.json",
        "spiderplot_news.json",
    ]

    base_url = "https://political-dashboard.com/json_files/"

    data = await utils.get_data_from_endpoints(
        session, endpoints, base_url, fetch_single
    )
    return data


async def fetch_single(session: ClientSession, url: str) -> Dict:
    async with session.get(url) as response:
        data = await response.json(content_type=None)

    filename = await utils.get_filename_from_url(url)
    if filename == "topics_news":
        data_type = "topics"
    elif filename == "news_party_attention":
        data_type = "attention"
    elif filename == "spiderplot_news":
        data_type = "topics_by_media_source"
    transformed_data = preprocess.transform(data, data_type)
    return transformed_data
