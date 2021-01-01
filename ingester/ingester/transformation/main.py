import re
from ast import literal_eval
from datetime import datetime
from typing import Callable, Dict, List, Union


def transform(
    data: Union[Dict, str], transform_items_func: Callable, key: str, date: datetime
) -> Dict:
    transformed_items: List[Dict] = transform_items_func(data)
    transformed_data = {
        "key": key,
        "date": data,
        "items": transformed_items,
    }
    return transformed_data


def transform_items_subset(data: Dict) -> List[Dict]:
    items: List[Dict] = data["chart"]
    transformed_items: List[Dict] = [
        {"text": i["text"], "count": i["count"]} for i in items
    ]
    return transformed_items


def transform_items_none(data: Dict) -> List[Dict]:
    return data["chart"]


def transform_items_counter(data: Dict) -> List[Dict]:
    count = data["chart"][0]["1"]["count"]
    return [{"count": count}]


def transform_items_regions(data: Dict) -> List[Dict]:
    geometries: List[Dict] = data["objects"]["DEU_adm1"]["geometries"]
    transformed_items: List[Dict] = [extract_shares(geometries, i) for i in range(16)]
    return transformed_items


def extract_shares(geometries: List[Dict], i: int) -> Dict:
    state: str = geometries[i]["properties"]["NAME_1"]
    share: List[float] = geometries[i]["properties"]["ads"]
    parties = ["AfD", "CDU_CSU", "FDP", "Gruenen", "Linke", "SPD"]
    party_shares = {party: share[i] for i, party in enumerate(parties)}
    return {"state": state, "parties": party_shares}


def transform_items_js(data: str, keys: List) -> List[Dict]:
    items: List[Dict] = parse_js(data)
    transformed_items: List[Dict] = [{key: i[key] for key in keys} for i in items]
    return transformed_items


def transform_items_ads_impressions(data: str) -> List[Dict]:
    items: List[Dict] = parse_js(data)
    transformed_items: List[Dict] = [convert_item_ads_impressions(i) for i in items]
    return transformed_items


def parse_js(blob: str) -> List[Dict]:
    start: int = blob.find("[")
    end: int = blob.find("]")
    blob = blob[start : end + 1]
    blob = blob.replace("\\u200b", "")
    blob = re.sub(r"\s\s", r"", blob)
    blob = re.sub(r",\s(\w*):", r',"\1":', blob)
    items: List[Dict] = literal_eval(blob)
    return items


def convert_item_ads_impressions(item: Dict) -> Dict:
    converted_item = {
        "advertiser": item["advertiser"],
        "lower_bound": str_to_int(item["lower bound"]),
        "upper_bound": str_to_int(item["upper bound"]),
        "lower_bound_spending": str_to_int(item["lower bound spending (€)"]),
        "upper_bound_spending": str_to_int(item["lower bound spending (€)"]),
    }
    return converted_item


def str_to_int(input: str) -> int:
    return int(input.replace(",", ""))


def transform_items_topics(data: Dict) -> List[Dict]:
    items: List = data["children"]
    transformed_items: List[Dict] = [convert_item_topics(i) for i in items]
    return transformed_items


def convert_item_topics(item: Dict) -> Dict:
    cluster_name: str = item["name"]
    cluster_share: float = item["value"]
    keywords: List[str] = item["name"].split(",")
    keywords_shares: List[float] = item["nameImportance"]
    keywords_dict = dict(zip(keywords, keywords_shares))
    converted_item = {
        "cluster_name": cluster_name,
        "cluster_share": cluster_share,
        "keywords": keywords_dict,
    }
    return converted_item
