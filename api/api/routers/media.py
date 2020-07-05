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
            models.URLsResponse,
            models.MediaAttentionResponse,
            models.MediaTopicsResponse,
            models.MediaTopicyByMediaSourceResponse,
        ]
    ],
)
async def media(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({}, times)
    return await db.find_media(db_filter)


@router.get("/urls", response_model=List[models.URLsResponse])
async def media_urls(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "urls"}, times)
    return await db.find_media(db_filter)


@router.get("/attention", response_model=List[models.MediaAttentionResponse])
async def media_attention(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "attention"}, times)
    return await db.find_media(db_filter)


@router.get("/topics", response_model=List[models.MediaTopicsResponse])
async def media_topics(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "topics"}, times)
    return await db.find_media(db_filter)


@router.get(
    "/topics_by_media_source",
    response_model=List[models.MediaTopicyByMediaSourceResponse],
)
async def media_topics_by_media_source(
    db: DataBase = Depends(get_database), times: Dict = Depends(time_query)
):
    db_filter = generate_base_filter({"data_type": "topics_by_media_source"}, times)
    return await db.find_media(db_filter)
