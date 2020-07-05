import re
from ast import literal_eval
from datetime import datetime
from typing import Callable, Dict, List, Union


def transform(
    data: Union[Dict, str], transform_items_func: Callable, data_type: str
) -> Dict:
    transformed_items: List = transform_items_func(data)
    transformed_data = {
        "data_type": data_type,
        "time": datetime.now(),
        "items": transformed_items,
    }
    return transformed_data


def transform_items_subset(data: Dict) -> List[Dict]:
    transformed_items = [
        {"text": i["text"], "count": i["count"]} for i in data["chart"]
    ]
    return transformed_items


def transform_items_none(data: Dict) -> List[Dict]:
    return data["chart"]


def transform_items_counter(data: Dict) -> List[Dict]:
    return data["chart"][0]["1"]["count"]


def transform_items_regions(data: Dict) -> List[Dict]:
    geometries = data["objects"]["DEU_adm1"]["geometries"]
    transformed_items = [extract_shares(geometries, i) for i in range(16)]
    return transformed_items


def extract_shares(geometries: List, i: int) -> Dict:
    state = geometries[i]["properties"]["NAME_1"]
    share = geometries[i]["properties"]["ads"]
    parties = ["AfD", "CDU/CSU", "FDP", "Gruenen", "Linke", "SPD"]
    party_shares = {party: share[i] for i, party in enumerate(parties)}
    return {"state": state, "parties": party_shares}


def transform_items_js(data: str, keys: List) -> List[Dict]:
    items = parse_js(data)
    transformed_items = [{key: item[key] for key in keys} for item in items]
    return transformed_items


def parse_js(blob: str) -> List[Dict]:
    start, end = blob.find("["), blob.rfind("]")
    blob = blob[start : end + 1]
    blob = blob.replace("\\u200b", "")
    blob = re.sub(r"\s\s", r"", blob)
    blob = re.sub(r",\s(\w*):", r',"\1":', blob)
    items = literal_eval(blob)
    return items


def transform_items_ads_impressions(data: str) -> List[Dict]:
    items = parse_js(data)
    transformed_items = [convert_item_ads_impressions(i) for i in items]
    return transformed_items


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
    items = data["children"]
    transformed_items = [convert_item_topics(i) for i in items]
    return transformed_items


def convert_item_topics(item: Dict) -> Dict:
    cluster_name = item["name"]
    cluster_share = item["value"]
    keywords = item["name"].split(",")
    keywords_shares = item["nameImportance"]
    keywords_dict = dict(zip(keywords, keywords_shares))
    converted_item = {
        "cluster_name": cluster_name,
        "cluster_share": cluster_share,
        "keywords": keywords_dict,
    }
    return converted_item
