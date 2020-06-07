from typing import List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DataBase, get_database

router = APIRouter()


@router.get(
    "",
    response_model=List[
        Union[models.MediaAttentionResponse, models.MediaTopicyByMediaSourceResponse]
    ],
)
async def media(db: DataBase = Depends(get_database)):
    return await db.find_media()


@router.get(
    "/attention", response_model=List[models.MediaAttentionResponse],
)
async def media_attention(db: DataBase = Depends(get_database)):
    return await db.find_media({"data_type": "attention"})


@router.get(
    "/topics_by_media_source",
    response_model=List[models.MediaTopicyByMediaSourceResponse],
)
async def media_topics_by_media_source(db: DataBase = Depends(get_database),):
    return await db.find_media({"data_type": "topics_by_media_source"})
