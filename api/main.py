from typing import List, Union

from fastapi import FastAPI, Query
from motor.motor_asyncio import AsyncIOMotorClient

from api import models, utils

app = FastAPI()


def setup_db(host_name, drop_all=False):
    client = AsyncIOMotorClient(host=host_name)
    db = client["database"]
    if drop_all:
        client.drop_database("database")
    twitter_col = db["twitter"]
    facebook_col = db["facebook"]
    media_col = db["media"]
    return twitter_col, facebook_col, media_col


twitter_col, facebook_col, media_col = setup_db("172.17.0.2")


# Twitter


@app.get(
    "/twitter",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
    tags=["twitter"],
)
async def twitter():
    return await utils.get_cleaned_docs(twitter_col)


@app.get(
    "/twitter/hashtags",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
    tags=["twitter"],
)
async def twitter_hashtags(
    party: str = Query(None, description="Abbreviated name of party", min_length=3)
):
    if party == None:
        return await utils.get_cleaned_docs(twitter_col, {"data_type": "hashtags"})
    else:
        return await utils.get_cleaned_docs(
            twitter_col, {"data_type": "hashtags", "party": party}
        )


# Facebook


@app.get(
    "/facebook",
    response_model=List[
        Union[
            models.SimpleFacebookResponse,
            models.FacebookReactionsReponse,
            models.FacebookSentimentResponse,
            models.FacebookAdsResponse,
        ]
    ],
    tags=["facebook"],
)
async def facebook():
    return await utils.get_cleaned_docs(facebook_col)


@app.get(
    "/facebook/posts",
    response_model=List[models.SimpleFacebookResponse],
    tags=["facebook"],
)
async def facebook_posts():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "posts"})


@app.get(
    "/facebook/shares",
    response_model=List[models.SimpleFacebookResponse],
    tags=["facebook"],
)
async def facebook_shares():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "shares"})


@app.get(
    "/facebook/likes",
    response_model=List[models.SimpleFacebookResponse],
    tags=["facebook"],
)
async def facebook_likes():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "likes"})


@app.get(
    "/facebook/reactions",
    response_model=List[models.FacebookReactionsReponse],
    tags=["facebook"],
)
async def facebook_reactions():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "reactions"})


@app.get(
    "/facebook/sentiment",
    response_model=List[models.FacebookSentimentResponse],
    tags=["facebook"],
)
async def facebook_sentiment():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "sentiment"})


@app.get(
    "/facebook/ads", response_model=List[models.FacebookAdsResponse], tags=["facebook"]
)
async def facebook_ads():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "ads"})


# Media


@app.get(
    "/media",
    response_model=List[
        Union[models.MediaAttentionResponse, models.MediaTopicyByMediaSourceResponse,]
    ],
    tags=["media"],
)
async def media():
    return await utils.get_cleaned_docs(media_col)


@app.get(
    "/media/attention",
    response_model=List[models.MediaAttentionResponse],
    tags=["media"],
)
async def media_attention():
    return await utils.get_cleaned_docs(media_col, {"data_type": "attention"})


@app.get(
    "/media/topics_by_media_source",
    response_model=List[models.MediaTopicyByMediaSourceResponse],
    tags=["media"],
)
async def media_topics_by_media_source():
    return await utils.get_cleaned_docs(
        media_col, {"data_type": "topics_by_media_source"}
    )
