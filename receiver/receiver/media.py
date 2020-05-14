from receiver import utils


async def get_data(session):
    endpoints = [
        # "topics_news.json",
        "news_party_attention.json",
        "spiderplot_news.json",
    ]

    base_url = "https://political-dashboard.com/json_files/"

    data = await utils.get_data_from_endpoints(session, endpoints, base_url, fetch)
    return data


async def fetch(session, url):
    async with session.get(url) as response:
        data = await response.json()

    filename = await utils.get_filename_from_url(url)
    if filename == "topics_news":
        data_type = "topics"
    elif filename == "news_party_attention":
        data_type = "attention"
    elif filename == "spiderplot_news":
        data_type = "topics_by_media_source"
    transformed_data = await transform(data, data_type)
    return transformed_data


async def transform(data, data_type):
    transformed_data = {"data_type": data_type}
    if data_type == "topics":
        transformed_data["items"] = data["children"]
    else:
        transformed_data["items"] = data["chart"]
    return transformed_data
