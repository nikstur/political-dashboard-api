from typing import List, Dict, Union

from aiohttp import ClientSession

from receiver import utils


async def get_data(session: ClientSession) -> List[Dict]:
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

    data = await utils.get_data_from_endpoints(session, endpoints, base_url, fetch)
    return data


async def fetch(session: ClientSession, url: str) -> Dict:
    async with session.get(url) as response:
        data = await response.json()

    filename = await utils.get_filename_from_url(url)
    if filename == "hashtags":
        party = None
    else:
        party = filename
    transformed_data = await transform(data, party)
    return transformed_data


async def transform(data: Dict, party: Union[str, None]) -> Dict:
    data_type = "hashtags"
    transformed_data = {
        "data_type": data_type,
        "items": data["chart"],
    }
    if party != None:
        transformed_data["party"] = party
    return transformed_data
