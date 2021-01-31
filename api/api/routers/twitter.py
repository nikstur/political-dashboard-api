from typing import Dict, List, Union

from fastapi import APIRouter, Depends, Query

from .. import models
from ..database import DataBase
from ..dependencies import db_conn, time_query

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
    db: DataBase = Depends(db_conn), time_query: Dict = Depends(time_query)
):
    """Data from all /twitter/* endpoints."""
    return await db.find(collection, {}, time_query)


@router.get(
    "/urls",
    response_model=List[models.URLsResponse],
)
async def urls(
    db: DataBase = Depends(db_conn),
    time_query: Dict = Depends(time_query),
):
    """URLs used in tweets.

    URLs pointing to other tweets, to social media sites (Facebook, Youtube,
    Instagram), or to Google/Bing search results are not included.
    """
    return await db.find(collection, {"key": "urls"}, time_query)


@router.get(
    "/hashtags",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def hashtags(
    db: DataBase = Depends(db_conn),
    time_query: Dict = Depends(time_query),
    party: str = Query(None, description="Abbreviated name of party", min_length=3),
):
    """Number of times a hashtag is used by supporters of a specific party.

    A supporter of a party is someone who has retweeted posts from this
    party at least 5 times. A user can be a supporter of multiple parties.
    """
    filters = {"key": "hashtags"}
    if party:
        filters.update({"party": party})
    return await db.find(collection, filters, time_query)


@router.get(
    "/hashtags_by_party",
    response_model=List[models.TwitterHashtagsByPartyResponse],
)
async def hashtags_by_party(
    db: DataBase = Depends(db_conn),
    time_query: Dict = Depends(time_query),
):
    """Share of tweets using the hashtag by supporters of each party.

    The returned numbers are the share of all tweets that use this hashtag. Thus the
    numbers for one hashtag always sum up to 1. The top ten tweets of the day are
    returned. This is intended to show how often a hashtag is used by supporters of
    the different parties. In the response example, the hashtag #seehofer is used most
    (38% of all usage) by supporters of AfD.
    """
    return await db.find(collection, {"key": "hashtags_by_party"}, time_query)
