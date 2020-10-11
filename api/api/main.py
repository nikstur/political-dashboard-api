from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from .database import database_connection
from .dependencies import api_key_query
from .routers import administration, facebook, media, twitter

app = FastAPI(
    title="API for political-dashboard.com",
    description="REST-API to programmatically access data from political-dashboard.com.",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
    default_response_class=ORJSONResponse,
    on_startup=[database_connection.connect],
    on_shutdown=[database_connection.disconnect],
)


app.include_router(
    administration.router, prefix="/administration", tags=["Administration"]
)
app.include_router(
    facebook.router,
    prefix="/facebook",
    tags=["Facebook"],
    dependencies=[Depends(api_key_query)],
)
app.include_router(
    media.router, prefix="/media", tags=["Media"], dependencies=[Depends(api_key_query)]
)
app.include_router(
    twitter.router,
    prefix="/twitter",
    tags=["Twitter"],
    dependencies=[Depends(api_key_query)],
)
