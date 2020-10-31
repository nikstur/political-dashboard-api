from datetime import date, datetime, time, timedelta
from typing import Optional, Tuple

from fastapi import Query
from starlette.exceptions import HTTPException

from .database import DataBase, database_connection

# Time


async def time_query(
    start_date: date = Query(date.today(), description="Start date in UTC (ISO 8601)"),
    end_date: date = Query(date.today(), description="End date in UTC (ISO 8601)"),
) -> Optional[dict]:
    if not start_date or not end_date:
        raise HTTPException(status_code=403, detail="Time span MUST be provided.")
    elif (end_date - date.today()) >= timedelta(days=1):
        raise HTTPException(status_code=418, detail="The future cannot be queried.")
    else:
        # Add day to end_date so that data before 00h of the next day is retrieved
        end_date += timedelta(days=1)
        time_delta = end_date - start_date
        if time_delta.days <= 10:
            time_filter = _construct_filter_from_date(start_date, end_date)
            return time_filter
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid time span. Maximum is 10 days.",
            )


def _construct_filter_from_date(start_date: date, end_date: date) -> dict:
    start_datetime, end_datetime = _transform_date_to_datetime(start_date, end_date)
    time_filter = _construct_filter_from_datetimes(start_datetime, end_datetime)
    return time_filter


def _transform_date_to_datetime(
    start_date: date, end_date: date
) -> Tuple[datetime, datetime]:
    start_datetime = datetime.combine(start_date, time())
    end_datetime = datetime.combine(end_date, time())
    return start_datetime, end_datetime


def _construct_filter_from_datetimes(
    start_datetime: datetime, end_datetime: datetime
) -> dict:
    time_filter = {"date": {"$gte": start_datetime, "$lt": end_datetime}}
    return time_filter


# Databases


def db_conn() -> DataBase:
    return database_connection.db
