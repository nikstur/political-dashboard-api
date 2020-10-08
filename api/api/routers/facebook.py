from typing import Dict, List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DBContent
from ..dependencies import db_content_conn, time_query

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
    db: DBContent = Depends(db_content_conn),
    time_filter: Dict = Depends(time_query),
):
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
async def facebook_ads(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    keys_ads = ["ads_by_advertiser", "ads_impressions", "ads_regions", "ads_count"]
    return await db.find(collection, {"key": {"$in": keys_ads}}, time_filter)


@router.get(
    "/ads/by_advertiser", response_model=List[models.FacebookAdsByAdvertiserResponse]
)
async def facebook_ads_by_advertiser(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "ads_by_advertiser"}, time_filter)


@router.get(
    "/ads/impressions", response_model=List[models.FacebookAdsImpressionsResponse]
)
async def facebook_ads_impressions(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "ads_impressions"}, time_filter)


@router.get("/ads/regions", response_model=List[models.FacebookAdsRegionsResponse])
async def facebook_ads_regions(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "ads_regions"}, time_filter)


@router.get("/ads/count", response_model=List[models.FacebookAdsCountResponse])
async def facebook_ads_count(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "ads_count"}, time_filter)


@router.get(
    "/reactions",
    response_model=List[models.FacebookReactionsReponse],
)
async def facebook_reactions(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "reactions"}, time_filter)


@router.get(
    "/sentiment",
    response_model=List[models.FacebookSentimentResponse],
)
async def facebook_sentiment(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "sentiment"}, time_filter)


@router.get(
    "/posts",
    response_model=List[models.SimpleFacebookResponse],
)
async def facebook_posts(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "posts"}, time_filter)


@router.get(
    "/shares",
    response_model=List[models.SimpleFacebookResponse],
)
async def facebook_shares(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "shares"}, time_filter)


@router.get(
    "/likes",
    response_model=List[models.SimpleFacebookResponse],
)
async def facebook_likes(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "likes"}, time_filter)
