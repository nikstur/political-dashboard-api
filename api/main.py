import json
from typing import List, Union

from fastapi import FastAPI, Query
from pymongo import MongoClient

from api import models, utils


app = FastAPI()

client = MongoClient(host="172.17.0.2")
db = client["database"]
twitter_col = db["twitter"]
facebook_col = db["facebook"]
media_col = db["media"]


@app.get("/")
async def root():
    return {"message": "Not yet implemented"}


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
async def hashtags(
    party: str = Query(None, description="Abbreviated name of party", min_length=3)
):
    if party == None:
        return utils.get_cleaned_docs(twitter_col, {"data_type": "hashtags"})
    else:
        return utils.get_cleaned_docs(
            twitter_col, {"data_type": "hashtags", "party": party}
        )


@app.get("/twitter/urls", response_model=models.TwitterURLResponse)
async def urls():
    return {"message": "Not yet implemented"}


@app.get("/facebook")
async def facebook():
    return {"message": "Not yet implemented"}


@app.get("/media")
async def media():
    return {"message": "Not yet implemented"}
