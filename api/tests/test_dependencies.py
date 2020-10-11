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


# When connect() method has not been called on DataBase AttributeError should be raised


def test_db_content_conn():
    with pytest.raises(AttributeError):
        dependencies.db_content_conn()


def test_db_admin_conn():
    with pytest.raises(AttributeError):
        dependencies.db_content_conn()


@pytest.fixture
def db_admin():
    class DBAdmin:
        async def find(self, collection, identifier):
            data = {
                1: {
                    "hash": "$2b$12$7pmPKz6uqV5DIFR7b7R0IuWXND0WdPQDM/1neOf.oTJXclqPd.ReW",
                    "can_create_token": True,
                },
                2: {
                    "hash": "$2b$12$OzOQm7lmrvcYmAeaIjsuruJSa2N71I6rhK16mMqSW54tSDXPERrm.",
                    "can_create_token": False,
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


@pytest.mark.parametrize(
    "api_key",
    [
        "1-49e04d40093d55aa6cd2ba679a7e1486",  # Wrong hash
        "2-49e04d40093d55aa5cd2ba679a7e1486",  # Correct hash with wrong identifier
        "3-49e04d40093d55aa5cd2ba679a7e1486",  # Correct hash with unknown id
    ],
)
@pytest.mark.asyncio
async def test_api_key_query_exceptional_input(api_key, db_admin):
    with pytest.raises(HTTPException) as excinfo:
        await dependencies.api_key_query(api_key, db_admin)
    assert "Not authenticated" in str(excinfo)


@pytest.mark.asyncio
async def test_admin_api_key_query_acceptable_input(db_admin):
    api_key_input = "1-49e04d40093d55aa5cd2ba679a7e1486"
    api_key_output = await dependencies.admin_api_key_query(api_key_input, db_admin)
    assert api_key_input == api_key_output


@pytest.mark.asyncio
async def test_admin_api_key_query_exceptional_input(db_admin):
    # Correct id and hash with wrong perms
    api_key = "2-49fcde3548d7aaf096017a4b19877432"

    with pytest.raises(HTTPException) as excinfo:
        await dependencies.admin_api_key_query(api_key, db_admin)
    assert "Insufficient rights to access this resource" in str(excinfo)
