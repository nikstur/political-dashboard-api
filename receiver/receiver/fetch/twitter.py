from typing import Dict, List

from aiohttp import ClientSession

from . import utils
from .preprocess import twitter as preprocess


async def twitter(session: ClientSession) -> List[Dict]:
    endpoints = [
        "hashtags.json",
        "CSU.json",
        "SPD.json",
        "CDU.json",
        "AfD.json",
        "FDP.json",
        "Gruenen.json",
        "Linke.json",
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
    if filename == "hashtags":
        party = None
    else:
        party = filename
    transformed_data = preprocess.transform(data, party)
    return transformed_data
