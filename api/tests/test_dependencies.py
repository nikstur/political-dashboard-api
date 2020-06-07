from datetime import datetime

import pytest
from api import dependencies


@pytest.mark.parametrize(
    "start_time,end_time,expected",
    [
        (None, None, None),
        (None, datetime(2020, 6, 8), None),
        (datetime(2020, 6, 7), None, None),
        (
            datetime(2020, 6, 7),
            datetime(2020, 6, 8),
            {"$gte": datetime(2020, 6, 7), "$lte": datetime(2020, 6, 8)},
        ),
    ],
)
@pytest.mark.asyncio
async def test_time_query(start_time, end_time, expected):
    times = await dependencies.time_query(start_time, end_time)
    assert times == expected
