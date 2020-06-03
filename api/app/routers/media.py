from typing import List, Union

from fastapi import APIRouter

from .. import database, models

router = APIRouter()

media_col = database.get_collection("media")
find_and_clean = database.create_find_and_clean(media_col)


@router.get(
    "",
    response_model=List[
        Union[models.MediaAttentionResponse, models.MediaTopicyByMediaSourceResponse]
    ],
)
async def media():
    return await find_and_clean()


@router.get(
    "/attention", response_model=List[models.MediaAttentionResponse],
)
async def media_attention():
    return await find_and_clean({"data_type": "attention"})


@router.get(
    "/topics_by_media_source",
    response_model=List[models.MediaTopicyByMediaSourceResponse],
)
async def media_topics_by_media_source():
    return await find_and_clean({"data_type": "topics_by_media_source"})
