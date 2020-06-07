from typing import Dict, List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DataBase, get_database
from ..dependencies import time_query

router = APIRouter()


@router.get(
    "",
    response_model=List[
        Union[models.MediaAttentionResponse, models.MediaTopicyByMediaSourceResponse]
    ],
)
async def media(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {}
    if times:
        db_filter["time"] = times
    return await db.find_media(db_filter)


@router.get("/attention", response_model=List[models.MediaAttentionResponse])
async def media_attention(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {"data_type": "attention"}
    if times:
        db_filter["time"] = times
    return await db.find_media(db_filter)


@router.get(
    "/topics_by_media_source",
    response_model=List[models.MediaTopicyByMediaSourceResponse],
)
async def media_topics_by_media_source(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter: Dict = {"data_type": "topics_by_media_source"}
    if times:
        db_filter["time"] = times
    return await db.find_media(db_filter)
