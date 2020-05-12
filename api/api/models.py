from typing import List, Union

from pydantic import BaseModel


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
