from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .database import database
from .routers import facebook, media, twitter

app = FastAPI(
    title="API for political-dashboard.com",
    description="REST-API to programmatically access data from political-dashboard.com.",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
def startup():
    database.connect()


@app.on_event("shutdown")
def shutdown():
    database.disconnect()


app.include_router(facebook.router, prefix="/facebook", tags=["Facebook"])
app.include_router(media.router, prefix="/media", tags=["Media"])
app.include_router(twitter.router, prefix="/twitter", tags=["Twitter"])
