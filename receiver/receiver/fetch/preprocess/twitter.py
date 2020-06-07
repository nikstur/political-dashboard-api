from datetime import datetime
from typing import Dict, Union


def transform(data: Dict, party: Union[str, None]) -> Dict:
    data_type = "hashtags"
    transformed_data = {
        "data_type": data_type,
        "time": datetime.now(),
        "items": data["chart"],
    }
    if party:
        transformed_data["party"] = party
    return transformed_data
