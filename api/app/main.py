from fastapi import FastAPI

from .routers import twitter, facebook, media

app = FastAPI(
    title="API for political-dashboard.com",
    description="REST-API to programmatically access data from political-dashboard.com.",
    version="0.1.0",
)

app.include_router(twitter.router, prefix="/twitter", tags=["twitter"])
app.include_router(facebook.router, prefix="/facebook", tags=["facebook"])
app.include_router(media.router, prefix="/media", tags=["media"])
