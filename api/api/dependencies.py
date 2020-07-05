from datetime import date, datetime, time
from typing import Dict, Union

from fastapi import Query


async def time_query(
    start_time: date = Query(None, description="UTC start time in ISO 8601"),
    end_time: date = Query(None, description="UTC end time in ISO 8601"),
) -> Union[Dict[str, datetime], None]:
    if not start_time or not end_time:
        return None
    else:
        datetime_start = datetime.combine(start_time, time())
        datetime_end = datetime.combine(end_time, time())
        return {"$gte": datetime_start, "$lte": datetime_end}
