from typing import List, Union

from fastapi import APIRouter, Query

from .. import database, models

router = APIRouter()

facebook_col = database.get_collection("facebook")
find_and_clean = database.create_find_and_clean(facebook_col)


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
async def facebook():
    return await find_and_clean()


@router.get(
    "/posts", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_posts():
    return await find_and_clean({"data_type": "posts"})


@router.get(
    "/shares", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_shares():
    return await find_and_clean({"data_type": "shares"})


@router.get(
    "/likes", response_model=List[models.SimpleFacebookResponse],
)
async def facebook_likes():
    return await find_and_clean({"data_type": "likes"})


@router.get(
    "/reactions", response_model=List[models.FacebookReactionsReponse],
)
async def facebook_reactions():
    return await find_and_clean({"data_type": "reactions"})


@router.get(
    "/sentiment", response_model=List[models.FacebookSentimentResponse],
)
async def facebook_sentiment():
    return await find_and_clean({"data_type": "sentiment"})


@router.get("/ads", response_model=List[models.FacebookAdsResponse])
async def facebook_ads():
    return await find_and_clean({"data_type": "ads"})
