from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

# Twitter


class TwitterHashtagResponseBody(BaseModel):
    text: str = Field(..., example="corona")
    biased: int = Field(..., example=0)
    count: int = Field(..., example=231)
    hours: int = Field(..., example=1192)


class TwitterHashtagResponse(BaseModel):
    data_type: str = Field("hashtags", example="hashtags")
    time: datetime = Field(..., example=datetime.now())
    party: str = Field(None, example="AfD")
    items: List[TwitterHashtagResponseBody]


# Facebook


class SimpleFacebookResponseBody(BaseModel):
    text: str = Field(..., example="AfD")
    count: int = Field(..., example=96320)
    biased: int = Field(..., example=1)
    hours: int = Field(..., example=0)


class SimpleFacebookResponse(BaseModel):
    data_type: str = Field(..., example="likes")
    time: datetime = Field(..., example=datetime.now())
    items: List[SimpleFacebookResponseBody]


class FacebookReactionsReponseBody(BaseModel):
    text: str = Field(..., example="angry")
    AfD: float = Field(..., example=0.386357741700678)
    CDU: float = Field(..., example=0.06478919561249338)
    CSU: float = Field(..., example=0.13987216902910365)
    FDP: float = Field(..., example=0.14515935455340986)
    Gruenen: float = Field(..., example=0.032320637537282655)
    Linke: float = Field(..., example=0.17705580266004384)
    SPD: float = Field(..., example=0.054445098906988704)


class FacebookReactionsReponse(BaseModel):
    data_type: str = Field("reactions", example="reactions")
    time: datetime = Field(..., example=datetime.now())
    items: List[FacebookReactionsReponseBody]


class FacebookSentimentResponseBody(BaseModel):
    text: str = Field(..., example="AfD")
    posts: float = Field(..., example=-0.06287638888888888)


class FacebookSentimentResponse(BaseModel):
    data_type: str = Field("sentiment", example="sentiment")
    time: datetime = Field(..., example=datetime.now())
    items: List[FacebookSentimentResponseBody]


class FacebookAdsResponse(BaseModel):
    data_type: str = Field("ads", example="ads")
    time: datetime = Field(..., example=datetime.now())
    count: int = Field(..., example=2724)


# Media


class MediaAttentionResponseBody(BaseModel):
    text: str = Field(..., example="AfD")
    count: int = Field(..., example=319)
    biased: int = Field(..., example=1)
    hours: int = Field(..., example=0)


class MediaAttentionResponse(BaseModel):
    data_type: str = Field("attention", example="attention")
    time: datetime = Field(..., example=datetime.now())
    items: List[MediaAttentionResponseBody]


class MediaTopicyByMediaSourceResponseBody(BaseModel):
    text: str = Field(
        ..., example="frage,coronakrise,mal,zeiten,tag,beispiel,deutsche,kinder"
    )
    C: float = Field(..., example=0.11950506309309615)
    L: float = Field(..., example=0.1800593900953377)
    R: float = Field(..., example=0.10951601192300174)
    CL: float = Field(..., example=0.18137428891904606)
    CR: float = Field(..., example=0.12002624146426925)


class MediaTopicyByMediaSourceResponse(BaseModel):
    data_type: str = Field("topics_by_media_source", example="topics_by_media_source")
    time: datetime = Field(..., example=datetime.now())
    items: List[MediaTopicyByMediaSourceResponseBody]
