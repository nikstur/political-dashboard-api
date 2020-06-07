from datetime import datetime
from typing import Dict


def transform_counter(data: Dict, data_type: str) -> Dict:
    transformed_data = {
        "data_type": data_type,
        "time": datetime.now(),
        "count": data["chart"][0]["1"]["count"],
    }
    return transformed_data


def transform(data: Dict, data_type: str) -> Dict:
    transformed_data = {
        "data_type": data_type,
        "time": datetime.now(),
        "items": data["chart"],
    }
    return transformed_data
