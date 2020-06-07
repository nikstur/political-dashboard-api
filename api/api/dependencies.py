from datetime import datetime
from typing import Dict, Union

from fastapi import Query


async def time_query(
    start_time: datetime = Query(None, description="UTC start time in ISO 8601"),
    end_time: datetime = Query(None, description="UTC end time in ISO 8601"),
) -> Union[Dict[str, datetime], None]:
    if not start_time or not end_time:
        return None
    else:
        return {"$gte": start_time, "$lte": end_time}
