from typing import Dict, List, Union


def transform(data: Dict, party: Union[str, None]) -> Dict:
    data_type = "hashtags"
    transformed_data = {
        "data_type": data_type,
        "items": data["chart"],
    }
    if party != None:
        transformed_data["party"] = party
    return transformed_data
