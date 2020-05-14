from receiver import utils


async def get_data(session):
    endpoints = [
        "counter_ads.json",
        "fb_spiderplot.json",
        "fb_sentiment.json",
        "fb_posts.json",
        "fb_likes.json",
        "fb_shares.json",
    ]

    base_url = "https://political-dashboard.com/json_files/"

    data = await utils.get_data_from_endpoints(session, endpoints, base_url, fetch)
    return data


async def fetch(session, url):
    async with session.get(url) as response:
        data = await response.json()

    filename = await utils.get_filename_from_url(url)
    if filename == "counter_ads":
        data_type = "ads"
        transformed_data = await transform_counter(data, data_type)
    else:
        filename = filename[3:]
        if filename == "spiderplot":
            data_type = "reactions"
        else:
            data_type = filename
        transformed_data = await transform(data, data_type)
    return transformed_data


async def transform_counter(data, data_type):
    transformed_data = {
        "data_type": data_type,
        "count": data["chart"][0]["1"]["count"],
    }
    return transformed_data


async def transform(data, data_type):
    transformed_data = {"data_type": data_type, "items": data["chart"]}
    return transformed_data
