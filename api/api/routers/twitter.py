from typing import Dict, List, Union

from fastapi import APIRouter, Depends, Query

from .. import models
from ..database import DataBase, get_database
from ..dependencies import time_query
from ..logic import generate_base_filter

router = APIRouter()


@router.get(
    "",
    response_model=List[
        Union[
            models.URLsResponse,
            models.TwitterHashtagResponse,
            models.TwitterHashtagsByPartyResponse,
        ]
    ],
    response_model_exclude_unset=True,
)
async def twitter(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({}, times)
    return await db.find_twitter(db_filter)


@router.get(
    "/urls", response_model=List[models.URLsResponse],
)
async def twitter_urls(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query),
):
    db_filter = generate_base_filter({"data_type": "urls"}, times)
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


@router.get(
    "/hashtags_by_party", response_model=List[models.TwitterHashtagsByPartyResponse],
)
async def twitter_hashtags_by_party(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query),
):
    db_filter = generate_base_filter({"data_type": "hashtags_by_party"}, times)
    return await db.find_twitter(db_filter)
