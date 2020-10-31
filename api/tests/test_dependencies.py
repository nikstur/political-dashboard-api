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


# When connect() method has not been called on DataBase, AttributeError should be raised


def test_db_conn():
    with pytest.raises(AttributeError):
        dependencies.db_conn()
