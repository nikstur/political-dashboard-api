from datetime import date, datetime, time
from typing import Dict, Union

from fastapi import Query

from . import database


async def time_query(
    start_date: date = Query(None, description="Start date in UTC (ISO 8601)"),
    end_date: date = Query(None, description="End date in UTC (ISO 8601)"),
) -> Union[Dict[str, Dict[str, datetime]], None]:
    if not start_date or not end_date:
        return None
    else:
        start_datetime: datetime = datetime.combine(start_date, time())
        end_datetime: datetime = datetime.combine(end_date, time())
        time_filter: Dict = {"time": {"$gte": start_datetime, "$lte": end_datetime}}
        return time_filter


def db_connection() -> database.DataBase:
    return database.database
