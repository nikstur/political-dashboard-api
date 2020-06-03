from typing import Any

import orjson
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routers import facebook, media, twitter


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(
    title="API for political-dashboard.com",
    description="REST-API to programmatically access data from political-dashboard.com.",
    version="0.1.0",
    default_response_class=ORJSONResponse,
)

app.include_router(twitter.router, prefix="/twitter", tags=["twitter"])
app.include_router(facebook.router, prefix="/facebook", tags=["facebook"])
app.include_router(media.router, prefix="/media", tags=["media"])
