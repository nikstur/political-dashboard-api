from typing import Dict, List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DBContent
from ..dependencies import db_content_conn, time_query

router = APIRouter()

collection = "media"


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
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {}, time_filter)


@router.get("/urls", response_model=List[models.URLsResponse])
async def media_urls(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "urls"}, time_filter)


@router.get("/attention", response_model=List[models.MediaAttentionResponse])
async def media_attention(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "attention"}, time_filter)


@router.get("/topics", response_model=List[models.MediaTopicsResponse])
async def media_topics(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "topics"}, time_filter)


@router.get(
    "/topics_by_media_source",
    response_model=List[models.MediaTopicyByMediaSourceResponse],
)
async def media_topics_by_media_source(
    db: DBContent = Depends(db_content_conn), time_filter: Dict = Depends(time_query)
):
    return await db.find(collection, {"key": "topics_by_media_source"}, time_filter)
