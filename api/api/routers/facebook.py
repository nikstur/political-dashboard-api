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
            models.SimpleFacebookResponse,
            models.FacebookReactionsReponse,
            models.FacebookSentimentResponse,
            models.FacebookAdsResponse,
        ]
    ],
)
async def facebook(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query),
):
    db_filter: Dict = {}
    if times:
        db_filter["time"] = times
    return await db.find_facebook(db_filter)


@router.get(
    "/posts", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_posts(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {"data_type": "posts"}
    if times:
        db_filter["time"] = times
    return await db.find_facebook(db_filter)


@router.get(
    "/shares", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_shares(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {"data_type": "shares"}
    if times:
        db_filter["time"] = times
    return await db.find_facebook(db_filter)


@router.get(
    "/likes", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_likes(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {"data_type": "likes"}
    if times:
        db_filter["time"] = times
    return await db.find_facebook(db_filter)


@router.get(
    "/reactions", response_model=List[models.FacebookReactionsReponse],
)
async def facebook_reactions(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {"data_type": "reactions"}
    if times:
        db_filter["time"] = times
    return await db.find_facebook(db_filter)


@router.get(
    "/sentiment", response_model=List[models.FacebookSentimentResponse],
)
async def facebook_sentiment(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {"data_type": "sentiment"}
    if times:
        db_filter["time"] = times
    return await db.find_facebook(db_filter)


@router.get("/ads", response_model=List[models.FacebookAdsResponse])
async def facebook_ads(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {"data_type": "ads"}
    if times:
        db_filter["time"] = times
    return await db.find_facebook(db_filter)
