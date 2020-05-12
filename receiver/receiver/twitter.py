import asyncio
import json
from urllib.parse import urlparse

from pymongo import MongoClient
import aiohttp

from receiver import utils


async def get_twitter():
    async with aiohttp.ClientSession() as session:
        hashtags = await get_hashtags(session)
    return hashtags


async def get_hashtags(session):
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
    urls = [base_url + endpoint for endpoint in endpoints]
    hashtags = await utils.fetch_multiple(session, urls, fetch_hashtags)
    return hashtags


async def fetch_hashtags(session, url):
    parsed_url = urlparse(url)
    filename = parsed_url.path.split("/")[-1].split(".")[0]
    if filename == "hashtags":
        party = None
    else:
        party = filename
    async with session.get(url) as response:
        data = await response.json()
        transformed_data = await transform_hashtags_json(data, party)
    return transformed_data


async def transform_hashtags_json(data, party):
    data_type = "hashtags"
    transformed_data = {
        "data_type": data_type,
        "party": party,
        "items": data["chart"],
    }
    return transformed_data
