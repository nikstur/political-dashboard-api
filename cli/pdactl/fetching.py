import os
from configparser import ConfigParser
from typing import Dict

import requests
from requests import Response

from .config import ensure_config


def get_full_url(endpoint: str) -> str:
    config: ConfigParser = ensure_config()
    base_url: str = config["core"]["url"]
    stripped_url: str = base_url.rstrip("/")
    stripped_endpoint: str = endpoint.lstrip("/")
    full_url: str = f"{stripped_url}/{stripped_endpoint}"
    return full_url


def post(url: str, request_body) -> Dict:
    response: Response = requests.post(
        url, json=request_body, headers=authentification()
    )
    response_dict: Dict = response.json()
    return response_dict


def get(url: str) -> Dict:
    response: Response = requests.get(url, headers=authentification())
    response_dict: Dict = response.json()
    return response_dict


def authentification() -> Dict:
    return {"X-API-KEY": os.getenv("PDA_API_KEY")}
