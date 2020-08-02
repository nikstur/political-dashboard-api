from typing import Dict, List, Union

from fastapi import APIRouter, Depends, Query

from .. import models
from ..database import DBContent
from ..dependencies import db_content_conn, time_query

router = APIRouter()

collection = "twitter"


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
    db: DBContent = Depends(db_content_conn), time_query: Dict = Depends(time_query)
):
    return await db.find(collection, {}, time_query)


@router.get(
    "/urls", response_model=List[models.URLsResponse],
)
async def twitter_urls(
    db: DBContent = Depends(db_content_conn), time_query: Dict = Depends(time_query),
):
    return await db.find(collection, {"data_type": "urls"}, time_query)


@router.get(
    "/hashtags",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def twitter_hashtags(
    db: DBContent = Depends(db_content_conn),
    time_query: Dict = Depends(time_query),
    party: str = Query(None, description="Abbreviated name of party", min_length=3),
):
    party_filter = {"party": party}
    return await db.find(
        collection, {"data_type": "hashtags"}, time_query, party_filter
    )


@router.get(
    "/hashtags_by_party", response_model=List[models.TwitterHashtagsByPartyResponse],
)
async def twitter_hashtags_by_party(
    db: DBContent = Depends(db_content_conn), time_query: Dict = Depends(time_query),
):
    return await db.find(collection, {"data_type": "hashtags_by_party"}, time_query)
