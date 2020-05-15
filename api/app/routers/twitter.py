from typing import List, Union

from fastapi import APIRouter, Query

from .. import database, models

router = APIRouter()

twitter_col = database.get_collection("twitter")
find_and_clean = database.create_find_and_clean(twitter_col)


@router.get(
    "",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def twitter():
    return await find_and_clean()


@router.get(
    "/hashtags",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def twitter_hashtags(
    party: str = Query(None, description="Abbreviated name of party", min_length=3)
):
    if party == None:
        return await find_and_clean({"data_type": "hashtags"})
    else:
        return await find_and_clean({"data_type": "hashtags", "party": party})
