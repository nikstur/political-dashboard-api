from datetime import date, datetime, time, timedelta
from typing import Optional, Tuple

from fastapi import Depends, Query, Security
from fastapi.security import APIKeyHeader
from passlib.hash import bcrypt
from starlette.exceptions import HTTPException

from .database import DBAdmin, DBContent, database_connection

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
            time_filter = construct_filter_from_date(start_date, end_date)
            return time_filter
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid time span. Maximum is 10 days.",
            )


def construct_filter_from_date(start_date: date, end_date: date) -> dict:
    start_datetime, end_datetime = transform_date_to_datetime(start_date, end_date)
    time_filter = construct_filter_from_datetimes(start_datetime, end_datetime)
    return time_filter


def transform_date_to_datetime(
    start_date: date, end_date: date
) -> Tuple[datetime, datetime]:
    start_datetime = datetime.combine(start_date, time())
    end_datetime = datetime.combine(end_date, time())
    return start_datetime, end_datetime


def construct_filter_from_datetimes(
    start_datetime: datetime, end_datetime: datetime
) -> dict:
    time_filter = {"date": {"$gte": start_datetime, "$lt": end_datetime}}
    return time_filter


# Databases


def db_content_conn() -> DBContent:
    return database_connection.db_content


def db_admin_conn() -> DBAdmin:
    return database_connection.db_admin


# Security


async def api_key_query(
    api_key: str = Security(APIKeyHeader(name="X-API-Key")),
    db: DBAdmin = Depends(db_admin_conn),
):
    is_verified = await verify_key_hash(api_key, db)
    if not is_verified:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        return api_key


async def verify_key_hash(api_key: str, db: DBAdmin) -> bool:
    identifier_str, key = api_key.split("-")
    identifier = int(identifier_str)
    doc: dict = await db.find("api_keys", identifier)
    if doc:
        key_hash = doc["hash"]
        is_verified = bool(key_hash and bcrypt.verify(key, key_hash))
        return is_verified
    else:
        return False


async def admin_api_key_query(
    api_key: str = Depends(api_key_query), db: DBAdmin = Depends(db_admin_conn)
):
    can_create_token: bool = await verify_can_create_token(api_key, db)
    if can_create_token:
        return api_key
    else:
        raise HTTPException(
            status_code=403,
            detail="Insufficient rights to access this resource",
        )


async def verify_can_create_token(api_key: str, db: DBAdmin) -> bool:
    identifier: int = int(api_key.split("-")[0])
    doc: dict = await db.find("api_keys", identifier)
    if doc:
        can_create_token: bool = doc["can_create_token"]
        return can_create_token
    else:
        return False
