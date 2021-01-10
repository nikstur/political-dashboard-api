from typing import Dict, List, Union

from fastapi import APIRouter, Depends

from .. import models
from ..database import DataBase
from ..dependencies import db_conn, time_query

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
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Data from all /media/* endpoints"""
    return await db.find(collection, {}, time_filter)


@router.get("/urls", response_model=List[models.URLsResponse])
async def urls(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """URLs used in articles."""
    return await db.find(collection, {"key": "urls"}, time_filter)


@router.get("/attention", response_model=List[models.MediaAttentionResponse])
async def attention(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Number of times the names of parties are mentioned in articles"""
    return await db.find(collection, {"key": "attention"}, time_filter)


@router.get("/topics", response_model=List[models.MediaTopicsResponse])
async def topics(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Topics of articles.

    The topics are identified using
    [Latent Dirichlet Allocation](https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf)
    The cluster name is the combination of the 8 most important words found in the articles
    of the topic. An optimization algorithm is used to find the optimal
    number of topics and thus their number can vary each day. The `keywords`
    field contains the keywords and their importance according to the LDA
    algorithm.
    """
    return await db.find(collection, {"key": "topics"}, time_filter)


@router.get(
    "/topics_by_media_source",
    response_model=List[models.MediaTopicyByMediaSourceResponse],
)
async def topics_by_media_source(
    db: DataBase = Depends(db_conn), time_filter: Dict = Depends(time_query)
):
    """Share of articles from news sources categorized by political orientation."""
    return await db.find(collection, {"key": "topics_by_media_source"}, time_filter)
