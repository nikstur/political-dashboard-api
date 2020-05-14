from typing import List, Union

from fastapi import FastAPI, Query
from motor.motor_asyncio import AsyncIOMotorClient

from api import models, utils

app = FastAPI()

client = AsyncIOMotorClient(host="172.17.0.2")
# client = AsyncIOMotorClient(host="db")
db = client["database"]
twitter_col = db["twitter"]
facebook_col = db["facebook"]
media_col = db["media"]


# Twitter


@app.get("/twitter", response_model=List[models.TwitterHashtagResponse])
async def twitter():
    return await utils.get_cleaned_docs(twitter_col)


@app.get(
    "/twitter/hashtags",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
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
)
async def facebook():
    return await utils.get_cleaned_docs(facebook_col)


@app.get("/facebook/posts", response_model=List[models.SimpleFacebookResponse])
async def facebook_posts():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "posts"})


@app.get("/facebook/shares", response_model=List[models.SimpleFacebookResponse])
async def facebook_shares():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "shares"})


@app.get("/facebook/likes", response_model=List[models.SimpleFacebookResponse])
async def facebook_likes():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "likes"})


@app.get("/facebook/reactions", response_model=List[models.FacebookReactionsReponse])
async def facebook_reactions():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "reactions"})


@app.get("/facebook/sentiment", response_model=List[models.FacebookSentimentResponse])
async def facebook_sentiment():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "sentiment"})


@app.get("/facebook/ads", response_model=List[models.FacebookAdsResponse])
async def facebook_ads():
    return await utils.get_cleaned_docs(facebook_col, {"data_type": "ads"})


# Media


@app.get(
    "/media",
    response_model=List[
        Union[models.MediaAttentionResponse, models.MediaTopicyByMediaSourceResponse,]
    ],
)
async def media():
    return await utils.get_cleaned_docs(media_col)


@app.get("/media/attention", response_model=List[models.MediaAttentionResponse])
async def media_attention():
    return await utils.get_cleaned_docs(media_col, {"data_type": "attention"})


@app.get(
    "/media/topics_by_media_source",
    response_model=List[models.MediaTopicyByMediaSourceResponse],
)
async def media_topics_by_media_source():
    return await utils.get_cleaned_docs(
        media_col, {"data_type": "topics_by_media_source"}
    )
