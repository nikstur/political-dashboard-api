from typing import List

from fastapi import APIRouter, Depends, Query

from .. import models
from ..database import DataBase, get_database

router = APIRouter()


@router.get(
    "",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def twitter(db: DataBase = Depends(get_database)):
    return await db.find_twitter()


@router.get(
    "/hashtags",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def twitter_hashtags(
    party: str = Query(None, description="Abbreviated name of party", min_length=3),
    db: DataBase = Depends(get_database),
):
    if not party:
        return await db.find_twitter({"data_type": "hashtags"})
    else:
        return await db.find_twitter({"data_type": "hashtags", "party": party})
