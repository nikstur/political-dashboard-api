from typing import Dict, List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DataBase
from ..dependencies import db_conn, time_query

router = APIRouter()

collection = "facebook"


@router.get(
    "",
    response_model=List[
        Union[
            models.FacebookAdsByAdvertiserResponse,
            models.FacebookAdsImpressionsResponse,
            models.FacebookAdsRegionsResponse,
            models.FacebookAdsCountResponse,
            models.FacebookReactionsReponse,
            models.FacebookSentimentResponse,
            models.SimpleFacebookResponse,
        ]
    ],
)
async def facebook(
    db: DataBase = Depends(db_conn),
    time_filter: Dict = Depends(time_query),
):
    """Data from all /facebook/* endpoints."""
    return await db.find(collection, {}, time_filter)


@router.get(
    "/ads",
    response_model=List[
        Union[
            models.FacebookAdsByAdvertiserResponse,
            models.FacebookAdsImpressionsResponse,
            models.FacebookAdsRegionsResponse,
            models.FacebookAdsCountResponse,
        ]
    ],
)
async def ads(db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)):
    """Data from all /facebook/ads/* endpoints."""
    keys_ads = ["ads_by_advertiser", "ads_impressions", "ads_regions", "ads_count"]
    return await db.find(collection, {"key": {"$in": keys_ads}}, time_filter)


@router.get(
    "/ads/by_advertiser", response_model=List[models.FacebookAdsByAdvertiserResponse]
)
async def ads_by_advertiser(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Number of ads published by single advertisers."""
    return await db.find(collection, {"key": "ads_by_advertiser"}, time_filter)


@router.get(
    "/ads/impressions", response_model=List[models.FacebookAdsImpressionsResponse]
)
async def ads_impressions(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Effectiveness of ads measured by their impressions."""
    return await db.find(collection, {"key": "ads_impressions"}, time_filter)


@router.get("/ads/regions", response_model=List[models.FacebookAdsRegionsResponse])
async def ads_regions(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Published political ads per region (federal state)."""
    return await db.find(collection, {"key": "ads_regions"}, time_filter)


@router.get("/ads/count", response_model=List[models.FacebookAdsCountResponse])
async def ads_count(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Number of political ads currently active on Facebook."""
    return await db.find(collection, {"key": "ads_count"}, time_filter)


@router.get(
    "/reactions",
    response_model=List[models.FacebookReactionsReponse],
)
async def reactions(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Reactions to the pages of each political party."""
    return await db.find(collection, {"key": "reactions"}, time_filter)


@router.get(
    "/sentiment",
    response_model=List[models.FacebookSentimentResponse],
)
async def sentiment(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Sentiment of each party's posts."""
    return await db.find(collection, {"key": "sentiment"}, time_filter)


@router.get(
    "/posts",
    response_model=List[models.SimpleFacebookResponse],
)
async def posts(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Number of posts of each party page."""
    return await db.find(collection, {"key": "posts"}, time_filter)


@router.get(
    "/shares",
    response_model=List[models.SimpleFacebookResponse],
)
async def shares(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Number shares for each party."""
    return await db.find(collection, {"key": "shares"}, time_filter)


@router.get(
    "/likes",
    response_model=List[models.SimpleFacebookResponse],
)
async def likes(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Number of likes for each party"""
    return await db.find(collection, {"key": "likes"}, time_filter)
