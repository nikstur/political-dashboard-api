from typing import List, Union

from pydantic import BaseModel

# Twitter


class TwitterURLResponseBody(BaseModel):
    text: str


class TwitterURLResponse(BaseModel):
    data_type: str = "url"
    items: List[TwitterURLResponseBody]


class TwitterHashtagResponseBody(BaseModel):
    biased: int
    count: int
    hours: int
    text: str


class TwitterHashtagResponse(BaseModel):
    data_type: str = "hashtags"
    party: str = None
    items: List[TwitterHashtagResponseBody]


# Facebook


class SimpleFacebookResponseBody(BaseModel):
    text: str
    count: int
    biased: int
    hours: int


class SimpleFacebookResponse(BaseModel):
    data_type: str
    items: List[SimpleFacebookResponseBody]


class FacebookReactionsBody(BaseModel):
    text: str
    AfD: float
    CDU: float
    CSU: float
    FDP: float
    Gruenen: float
    Linke: float
    SPD: float


class FacebookReactionsReponse(BaseModel):
    data_type: str = "reactions"
    items: List[FacebookReactionsBody]


class FacebookSentimentBody(BaseModel):
    text: str
    posts: float


class FacebookSentimentResponse(BaseModel):
    data_type: str = "sentiment"
    items: List[FacebookSentimentBody]


class FacebookAdsResponse(BaseModel):
    data_type: str = "ads"
    count: int
