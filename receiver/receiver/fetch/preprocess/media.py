from datetime import datetime
from typing import Dict


def transform(data: Dict, data_type: str) -> Dict:
    transformed_data = {"data_type": data_type, "time": datetime.now()}
    if data_type == "topics":
        transformed_data["items"] = data["children"]
    else:
        transformed_data["items"] = data["chart"]
    return transformed_data
