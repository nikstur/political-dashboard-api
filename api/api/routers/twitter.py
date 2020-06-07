from typing import Dict, List

from fastapi import APIRouter, Depends, Query

from .. import models
from ..database import DataBase, get_database
from ..dependencies import time_query
from ..logic import generate_base_filter

router = APIRouter()


@router.get(
    "",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def twitter(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({}, times)
    return await db.find_twitter(db_filter)


@router.get(
    "/hashtags",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def twitter_hashtags(
    db: DataBase = Depends(get_database),
    times: Dict = Depends(time_query),
    party: str = Query(None, description="Abbreviated name of party", min_length=3),
):
    db_filter = generate_base_filter({"data_type": "hashtags"}, times)
    if party:
        db_filter["party"] = party
    return await db.find_twitter(db_filter)
