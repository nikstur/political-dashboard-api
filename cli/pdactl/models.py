from datetime import datetime

from pydantic import BaseModel


class KeyResponse(BaseModel):
    identifier: int
    can_create_token: bool
    created_by: int
    creation_date: datetime


class KeyAddResponse(KeyResponse):
    new_api_key: str
