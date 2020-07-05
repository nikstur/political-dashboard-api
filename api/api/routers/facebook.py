from typing import Dict, List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DataBase, get_database
from ..dependencies import time_query
from ..logic import generate_base_filter

router = APIRouter()


@router.get(
    "",
    response_model=List[
        Union[
            models.FacebookAdsResponse,
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
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query),
):
    db_filter = generate_base_filter({}, times)
    return await db.find_facebook(db_filter)


@router.get("/ads", response_model=List[models.FacebookAdsResponse])
async def facebook_ads(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "ads"}, times)
    return await db.find_facebook(db_filter)


@router.get(
    "/ads_impressions", response_model=List[models.FacebookAdsImpressionsResponse]
)
async def facebook_ads_impressions(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "ads_impressions"}, times)
    return await db.find_facebook(db_filter)


@router.get("/ads_regions", response_model=List[models.FacebookAdsRegionsResponse])
async def facebook_ads_regions(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "ads_regions"}, times)
    return await db.find_facebook(db_filter)


@router.get("/ads_count", response_model=List[models.FacebookAdsCountResponse])
async def facebook_ads_count(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "ads_count"}, times)
    return await db.find_facebook(db_filter)


@router.get(
    "/reactions", response_model=List[models.FacebookReactionsReponse],
)
async def facebook_reactions(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "reactions"}, times)
    return await db.find_facebook(db_filter)


@router.get(
    "/sentiment", response_model=List[models.FacebookSentimentResponse],
)
async def facebook_sentiment(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "sentiment"}, times)
    return await db.find_facebook(db_filter)


@router.get(
    "/posts", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_posts(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "posts"}, times)
    return await db.find_facebook(db_filter)


@router.get(
    "/shares", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_shares(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "shares"}, times)
    return await db.find_facebook(db_filter)


@router.get(
    "/likes", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_likes(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "likes"}, times)
    return await db.find_facebook(db_filter)
