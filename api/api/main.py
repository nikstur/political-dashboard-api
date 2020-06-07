from typing import Any

import orjson
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .database import database
from .routers import facebook, media, twitter


class ORJSONResponse(JSONResponse):
    """Orjson drop-in replacement for default JSON serializer"""

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(
    title="API for political-dashboard.com",
    description="REST-API to programmatically access data from political-dashboard.com.",
    version="0.1.0",
    redoc_url=None,
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
def startup():
    database.connect()


@app.on_event("shutdown")
def shutdown():
    database.disconnect()


app.include_router(twitter.router, prefix="/twitter", tags=["Twitter"])
app.include_router(facebook.router, prefix="/facebook", tags=["Facebook"])
app.include_router(media.router, prefix="/media", tags=["Media"])
