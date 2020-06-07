from typing import List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DataBase, get_database

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
async def facebook(db: DataBase = Depends(get_database)):
    return await db.find_facebook()


@router.get(
    "/posts", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_posts(db: DataBase = Depends(get_database)):
    return await db.find_facebook({"data_type": "posts"})


@router.get(
    "/shares", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_shares(db: DataBase = Depends(get_database)):
    return await db.find_facebook({"data_type": "shares"})


@router.get(
    "/likes", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_likes(db: DataBase = Depends(get_database)):
    return await db.find_facebook({"data_type": "likes"})


@router.get(
    "/reactions", response_model=List[models.FacebookReactionsReponse],
)
async def facebook_reactions(db: DataBase = Depends(get_database),):
    return await db.find_facebook({"data_type": "reactions"})


@router.get(
    "/sentiment", response_model=List[models.FacebookSentimentResponse],
)
async def facebook_sentiment(db: DataBase = Depends(get_database),):
    return await db.find_facebook({"data_type": "sentiment"})


@router.get("/ads", response_model=List[models.FacebookAdsResponse])
async def facebook_ads(db: DataBase = Depends(get_database)):
    return await db.find_facebook({"data_type": "ads"})
