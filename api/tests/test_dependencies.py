from datetime import date, datetime, timedelta

import pytest
from starlette.exceptions import HTTPException

from api import dependencies


@pytest.mark.asyncio
async def test_time_query_acceptable_input():
    start_date = date(2020, 6, 7)
    end_date = date(2020, 6, 8)
    expected = {"date": {"$gte": datetime(2020, 6, 7), "$lt": datetime(2020, 6, 9)}}

    time_filter = await dependencies.time_query(start_date, end_date)
    assert time_filter == expected


time_query_exceptional_test_data = [
    (
        date(2020, 6, 7),
        None,
        pytest.raises(HTTPException),
        "Time span MUST be provided",
    ),
    (
        None,
        date(2020, 6, 8),
        pytest.raises(HTTPException),
        "Time span MUST be provided",
    ),
    (None, None, pytest.raises(HTTPException), "Time span MUST be provided"),
    (
        date(2020, 6, 7),
        date(2020, 6, 17),
        pytest.raises(HTTPException),
        "Invalid time span. Maximum is 10 days.",
    ),
    (
        date.today(),
        date.today() + timedelta(days=1),
        pytest.raises(HTTPException),
        "The future cannot be queried.",
    ),
]


@pytest.mark.parametrize(
    "start_date,end_date,expected_raises,exception",
    time_query_exceptional_test_data,
)
@pytest.mark.asyncio
async def test_time_query_exceptional_input(
    start_date, end_date, expected_raises, exception
):
    with expected_raises as excinfo:
        await dependencies.time_query(start_date, end_date)
    assert exception in str(excinfo)


def test_construct_filter_from_date():
    start_date = date(2020, 6, 7)
    end_date = date(2020, 6, 8)
    expected = {"date": {"$gte": datetime(2020, 6, 7), "$lt": datetime(2020, 6, 8)}}

    time_filter = dependencies.construct_filter_from_date(start_date, end_date)
    assert time_filter == expected


def test_transform_date_to_datetime():
    start_date = date(2020, 6, 7)
    end_date = date(2020, 6, 8)
    expected_start_datetime = datetime(2020, 6, 7, 0, 0)
    expected_end_datetime = datetime(2020, 6, 8, 0, 0)

    start_datetime, end_datetime = dependencies.transform_date_to_datetime(
        start_date, end_date
    )
    assert start_datetime == expected_start_datetime
    assert end_datetime == expected_end_datetime


@pytest.fixture
def db_admin():
    class DBAdmin:
        async def find(self, collection, identifier):
            data = {
                1: {
                    "hash": "$2b$12$7pmPKz6uqV5DIFR7b7R0IuWXND0WdPQDM/1neOf.oTJXclqPd.ReW"
                },
            }
            return data.get(identifier)

    db_admin = DBAdmin()
    return db_admin


@pytest.mark.asyncio
async def test_api_key_query_acceptable_input(db_admin):
    api_key_input = "1-49e04d40093d55aa5cd2ba679a7e1486"
    api_key_output = await dependencies.api_key_query(api_key_input, db_admin)
    assert api_key_input == api_key_output


@pytest.mark.asyncio
async def test_api_key_query_exceptional_input(db_admin):
    api_key_input = "2-49e04d40093d55aa5cd2ba679a7e1486"
    with pytest.raises(HTTPException) as excinfo:
        await dependencies.api_key_query(api_key_input, db_admin)
    assert "Not authenticated" in str(excinfo)


@pytest.mark.parametrize(
    "api_key,expected",
    [
        ("1-49e04d40093d55aa5cd2ba679a7e1486", True),
        ("2-49e04d40093d55aa5cd2ba679a7e1486", False),
        ("1-49e04d40093d55aa6cd2ba679a7e1486", False),
    ],
)
@pytest.mark.asyncio
async def test_verify_key_hash(db_admin, api_key, expected):
    is_verified = await dependencies.verify_key_hash(api_key, db_admin)
    assert is_verified == expected
