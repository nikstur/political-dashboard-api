from typing import List, Union

from pydantic import BaseModel

# Twitter


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


class FacebookReactionsReponseBody(BaseModel):
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
    items: List[FacebookReactionsReponseBody]


class FacebookSentimentResponseBody(BaseModel):
    text: str
    posts: float


class FacebookSentimentResponse(BaseModel):
    data_type: str = "sentiment"
    items: List[FacebookSentimentResponseBody]


class FacebookAdsResponse(BaseModel):
    data_type: str = "ads"
    count: int


# Media


class MediaAttentionResponseBody(BaseModel):
    text: str
    count: int
    biased: int
    hours: int


class MediaAttentionResponse(BaseModel):
    data_type: str = "attention"
    items: List[MediaAttentionResponseBody]


class MediaTopicyByMediaSourceResponseBody(BaseModel):
    text: str
    C: float
    L: float
    R: float
    CL: float
    CR: float


class MediaTopicyByMediaSourceResponse(BaseModel):
    data_type: str = "topics_by_media_source"
    items: List[MediaTopicyByMediaSourceResponseBody]
