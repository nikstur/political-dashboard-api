import json
from typing import List, Union

from fastapi import FastAPI, Query
from pymongo import MongoClient

from api import models, utils


app = FastAPI()

# client = MongoClient(host="172.17.0.2")
client = MongoClient(host="db")
db = client["database"]
twitter_col = db["twitter"]
facebook_col = db["facebook"]
media_col = db["media"]


# Twitter


@app.get(
    "/twitter",
    response_model=List[
        Union[models.TwitterHashtagResponse, models.TwitterURLResponse]
    ],
)
async def twitter():
    return utils.get_cleaned_docs(twitter_col)


@app.get(
    "/twitter/hashtags",
    response_model=List[models.TwitterHashtagResponse],
    response_model_exclude_unset=True,
)
async def twitter_hashtags(
    party: str = Query(None, description="Abbreviated name of party", min_length=3)
):
    if party == None:
        return utils.get_cleaned_docs(twitter_col, {"data_type": "hashtags"})
    else:
        return utils.get_cleaned_docs(
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
    return utils.get_cleaned_docs(facebook_col)


@app.get("/facebook/posts", response_model=List[models.SimpleFacebookResponse])
async def facebook_posts():
    return utils.get_cleaned_docs(facebook_col, {"data_type": "posts"})


@app.get("/facebook/shares", response_model=List[models.SimpleFacebookResponse])
async def facebook_shares():
    return utils.get_cleaned_docs(facebook_col, {"data_type": "shares"})


@app.get("/facebook/likes", response_model=List[models.SimpleFacebookResponse])
async def facebook_likes():
    return utils.get_cleaned_docs(facebook_col, {"data_type": "likes"})


@app.get("/facebook/reactions", response_model=List[models.FacebookReactionsReponse])
async def facebook_reactions():
    return utils.get_cleaned_docs(facebook_col, {"data_type": "reactions"})


@app.get("/facebook/sentiment", response_model=List[models.FacebookSentimentResponse])
async def facebook_sentiment():
    return utils.get_cleaned_docs(facebook_col, {"data_type": "sentiment"})


@app.get("/facebook/ads", response_model=List[models.FacebookAdsResponse])
async def facebook_ads():
    return utils.get_cleaned_docs(facebook_col, {"data_type": "ads"})


# Media


@app.get("/media")
async def media():
    return {"message": "Not yet implemented"}
