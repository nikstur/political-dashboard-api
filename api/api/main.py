from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .database import database_connection
from .routers import facebook, media, twitter

app = FastAPI(
    title="API for political-dashboard.com",
    description=(
        "REST-API to access historical data from political-dashboard.com."
        " Please report issues at https://github.com/nikstur/political-dashboard-api/issues"
    ),
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
    default_response_class=ORJSONResponse,
    on_startup=[database_connection.connect],
    on_shutdown=[database_connection.disconnect],
)


app.include_router(
    facebook.router,
    prefix="/facebook",
    tags=["Facebook"],
)
app.include_router(media.router, prefix="/media", tags=["Media"])
app.include_router(
    twitter.router,
    prefix="/twitter",
    tags=["Twitter"],
)
