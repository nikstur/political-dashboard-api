from typing import Dict, List

from aiohttp import ClientSession

from . import utils
from .preprocess import facebook as preprocess


async def facebook(session: ClientSession) -> List[Dict]:
    endpoints = [
        "counter_ads.json",
        "fb_spiderplot.json",
        "fb_sentiment.json",
        "fb_posts.json",
        "fb_likes.json",
        "fb_shares.json",
    ]

    base_url = "https://political-dashboard.com/json_files/"

    data = await utils.get_data_from_endpoints(
        session, endpoints, base_url, fetch_single
    )
    return data


async def fetch_single(session: ClientSession, url: str) -> Dict:
    async with session.get(url) as response:
        data = await response.json()

    filename = await utils.get_filename_from_url(url)
    if filename == "counter_ads":
        data_type = "ads"
        transformed_data = preprocess.transform_counter(data, data_type)
    else:
        filename = filename[3:]
        if filename == "spiderplot":
            data_type = "reactions"
        else:
            data_type = filename
        transformed_data = preprocess.transform(data, data_type)
    return transformed_data
