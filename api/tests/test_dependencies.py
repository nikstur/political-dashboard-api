from datetime import date, datetime

import pytest
from api import dependencies


@pytest.mark.parametrize(
    "start_time,end_time,expected",
    [
        (None, None, None),
        (None, date(2020, 6, 8), None),
        (date(2020, 6, 7), None, None),
        (
            date(2020, 6, 7),
            date(2020, 6, 8),
            {"time": {"$gte": datetime(2020, 6, 7), "$lte": datetime(2020, 6, 8)}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_time_query(start_time, end_time, expected):
    time_filter = await dependencies.time_query(start_time, end_time)
    assert time_filter == expected
