from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .database import database_connection
from .metadata import load_desc, openapi_tags
from .routers import facebook, media, twitter

app = FastAPI(
    title="api.political-dashboard.com",
    description=load_desc("description.md"),
    version="0.1.0",
    docs_url=None,
    redoc_url="/",
    default_response_class=ORJSONResponse,
    on_startup=[database_connection.connect],
    on_shutdown=[database_connection.disconnect],
    openapi_tags=openapi_tags,
)

app.include_router(
    twitter.router,
    prefix="/twitter",
    tags=["Twitter"],
)

app.include_router(
    facebook.router,
    prefix="/facebook",
    tags=["Facebook"],
)
app.include_router(media.router, prefix="/media", tags=["Media"])
