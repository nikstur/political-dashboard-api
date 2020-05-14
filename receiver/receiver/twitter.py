from receiver import utils


async def get_data(session):
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


async def fetch(session, url):
    async with session.get(url) as response:
        data = await response.json()

    filename = utils.get_filename_from_url(url)
    if filename == "hashtags":
        party = None
    else:
        party = filename
    transformed_data = await transform(data, party)
    return transformed_data


async def transform(data, party):
    data_type = "hashtags"
    if party == None:
        transformed_data = {
            "data_type": data_type,
            "items": data["chart"],
        }
    else:
        transformed_data["party"] = party
    return transformed_data
