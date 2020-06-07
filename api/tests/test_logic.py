from datetime import datetime

import pytest
from api import logic


@pytest.mark.parametrize(
    "initial_filter,times,expected",
    [
        ({}, None, {}),
        ({"data_type": "hashtags"}, None, {"data_type": "hashtags"}),
        (
            {},
            {"$gte": datetime(2020, 6, 7), "$lte": datetime(2020, 6, 8)},
            {"time": {"$gte": datetime(2020, 6, 7), "$lte": datetime(2020, 6, 8)}},
        ),
        (
            {"data_type": "hashtags"},
            {"$gte": datetime(2020, 6, 7), "$lte": datetime(2020, 6, 8)},
            {
                "data_type": "hashtags",
                "time": {"$gte": datetime(2020, 6, 7), "$lte": datetime(2020, 6, 8)},
            },
        ),
    ],
)
def test_generate_base_filter(initial_filter, times, expected):
    db_filter = logic.generate_base_filter(initial_filter, times)
    assert db_filter == expected
