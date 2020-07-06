from typing import Dict, List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DataBase, get_database
from ..dependencies import time_query

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
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query),
):
    return await db.find_facebook({}, [time_filter])


@router.get("/ads", response_model=List[models.FacebookAdsResponse])
async def facebook_ads(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "ads"}, [time_filter])


@router.get(
    "/ads_impressions", response_model=List[models.FacebookAdsImpressionsResponse]
)
async def facebook_ads_impressions(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "ads_impressions"}, [time_filter])


@router.get("/ads_regions", response_model=List[models.FacebookAdsRegionsResponse])
async def facebook_ads_regions(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "ads_regions"}, [time_filter])


@router.get("/ads_count", response_model=List[models.FacebookAdsCountResponse])
async def facebook_ads_count(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "ads_count"}, [time_filter])


@router.get(
    "/reactions", response_model=List[models.FacebookReactionsReponse],
)
async def facebook_reactions(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "reactions"}, [time_filter])


@router.get(
    "/sentiment", response_model=List[models.FacebookSentimentResponse],
)
async def facebook_sentiment(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "sentiment"}, [time_filter])


@router.get(
    "/posts", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_posts(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "posts"}, [time_filter])


@router.get(
    "/shares", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_shares(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "shares"}, [time_filter])


@router.get(
    "/likes", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_likes(
    db: DataBase = Depends(get_database), time_filter: Dict = Depends(time_query)
):
    return await db.find_facebook({"data_type": "likes"}, [time_filter])
