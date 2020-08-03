import datetime
from typing import Dict, List

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    date: datetime.date = Field(..., example=datetime.date.today())


class URLsResponseBody(BaseModel):
    text: str = Field(
        ..., example="http://www.tagesschau.de/inland/toennis-gabriel-berater-101.html"
    )
    count: int = Field(..., example=5985)


class URLsResponse(BaseResponse):
    key: str = Field("urls", example="urls")
    items: List[URLsResponseBody]


# Administration


class AdministrationKeyResponse(BaseModel):
    identifier: int = Field(..., example=5)
    can_create_token: bool = Field(..., example=False)
    created_by: int = Field(..., example=1)
    creation_date: datetime.datetime = Field(..., example=datetime.datetime.utcnow())


class AdministrationAddKeyResponse(AdministrationKeyResponse):
    new_api_key: str = Field(..., example="5-0f63e1c9f67b0dd10kc5a309f98d7464")


# Facebook


class FacebookAdsByAdvertiserResponseBody(BaseModel):
    advertiser: str = Field("advertiser", example="FDP Berlin")
    count: int = Field(..., example=304)


class FacebookAdsByAdvertiserResponse(BaseResponse):
    key: str = Field("ads", example="ads")
    items: List[FacebookAdsByAdvertiserResponseBody]


class FacebookAdsImpressionsResponseBody(BaseModel):
    advertiser: str = Field("advertiser", example="Bundesregierung")
    lower_bound: int = Field(..., example=6815000)
    lower_bound_spending: int = Field(..., example=34100)
    upper_bound: int = Field(..., example=7859980)
    upper_bound_spending: int = Field(..., example=34100)


class FacebookAdsImpressionsResponse(BaseResponse):
    key: str = Field("ads_impressions", example="ads_impressions")
    items: List[FacebookAdsImpressionsResponseBody]


class FacebookAdsRegionsResponseBodyParties(BaseModel):
    AfD: float = Field(..., example=0.1195105731722062)
    CDU_CSU: float = Field(..., example=0.125)
    FDP: float = Field(..., example=0.12444536949598713)
    Gruenen: float = Field(..., example=0.0)
    Linke: float = Field(..., example=0.10391824117789662)
    SPD: float = Field(..., example=0.05724696128397787)


class FacebookAdsRegionsResponseBody(BaseModel):
    state: str = Field("state", example="Bayern")
    parties: FacebookAdsRegionsResponseBodyParties


class FacebookAdsRegionsResponse(BaseResponse):
    key: str = Field("ads_regions", example="ads_regions")
    items: List[FacebookAdsRegionsResponseBody]


class FacebookAdsCountResponseBody(BaseModel):
    count: int = Field(..., example=3294)


class FacebookAdsCountResponse(BaseResponse):
    key: str = Field("ads_count", example="ads_count")
    items: List[FacebookAdsCountResponseBody]


class FacebookReactionsReponseBody(BaseModel):
    text: str = Field(..., example="angry")
    AfD: float = Field(..., example=0.386357741700678)
    CDU: float = Field(..., example=0.06478919561249338)
    CSU: float = Field(..., example=0.13987216902910365)
    FDP: float = Field(..., example=0.14515935455340986)
    Gruenen: float = Field(..., example=0.032320637537282655)
    Linke: float = Field(..., example=0.17705580266004384)
    SPD: float = Field(..., example=0.054445098906988704)


class FacebookReactionsReponse(BaseResponse):
    key: str = Field("reactions", example="reactions")
    items: List[FacebookReactionsReponseBody]


class FacebookSentimentResponseBody(BaseModel):
    text: str = Field(..., example="AfD")
    posts: float = Field(..., example=-0.06287638888888888)


class FacebookSentimentResponse(BaseResponse):
    key: str = Field("sentiment", example="sentiment")
    items: List[FacebookSentimentResponseBody]


class SimpleFacebookResponseBody(BaseModel):
    text: str = Field(..., example="AfD")
    count: int = Field(..., example=96320)


class SimpleFacebookResponse(BaseResponse):
    key: str = Field(..., example="likes")
    items: List[SimpleFacebookResponseBody]


# Media


class MediaAttentionResponseBody(BaseModel):
    text: str = Field(..., example="AfD")
    count: int = Field(..., example=319)


class MediaAttentionResponse(BaseResponse):
    key: str = Field("attention", example="attention")
    items: List[MediaAttentionResponseBody]


class MediaTopicsResponseBody(BaseModel):
    cluster_name: str = Field(
        ...,
        example="söder,merz,ministerpräsident,cdu,laschet,csu,kanzlerkandidatur,chef",
    )
    cluster_share: float = Field(..., example=0.15755530934093848)
    keywords: Dict[str, float]


class MediaTopicsResponse(BaseResponse):
    key: str = Field("topics", example="topics")
    items: List[MediaTopicsResponseBody]


class MediaTopicyByMediaSourceResponseBody(BaseModel):
    text: str = Field(
        ..., example="frage,coronakrise,mal,zeiten,tag,beispiel,deutsche,kinder"
    )
    C: float = Field(..., example=0.11950506309309615)
    L: float = Field(..., example=0.1800593900953377)
    R: float = Field(..., example=0.10951601192300174)
    CL: float = Field(..., example=0.18137428891904606)
    CR: float = Field(..., example=0.12002624146426925)


class MediaTopicyByMediaSourceResponse(BaseResponse):
    key: str = Field("topics_by_media_source", example="topics_by_media_source")
    items: List[MediaTopicyByMediaSourceResponseBody]


# Twitter


class TwitterHashtagsByPartyResponseBody(BaseModel):
    text: str = Field(..., example="seehofer")
    AfD: float = Field(..., example=0.386357741700678)
    CDU: float = Field(..., example=0.06478919561249338)
    CSU: float = Field(..., example=0.13987216902910365)
    FDP: float = Field(..., example=0.14515935455340986)
    Gruenen: float = Field(..., example=0.032320637537282655)
    Linke: float = Field(..., example=0.17705580266004384)
    SPD: float = Field(..., example=0.054445098906988704)


class TwitterHashtagsByPartyResponse(BaseResponse):
    key: str = Field("hashtags_by_party", example="hashtags_by_party")
    items: List[TwitterHashtagsByPartyResponseBody]


class TwitterHashtagResponseBody(BaseModel):
    text: str = Field(..., example="corona")
    count: int = Field(..., example=231)


class TwitterHashtagResponse(BaseResponse):
    key: str = Field("hashtags", example="hashtags")
    party: str = Field(None, example="AfD")
    items: List[TwitterHashtagResponseBody]
