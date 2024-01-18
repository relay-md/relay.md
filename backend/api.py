# -*- coding: utf-8 -*-
import sentry_sdk
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from . import exceptions
from .config import get_config
from .database import Base, engine
from .routes.v1 import assets as v1_assets
from .routes.v1 import docs as v1_docs

# Setup sentry for alerting in case of exceptions
if get_config().SENTRY_DSN:
    sentry_sdk.init(
        dsn=get_config().SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

# Create all tables
Base.metadata.create_all(engine)

# Load metadata from yaml file
app = FastAPI(**get_config().FASTAPI_CONFIG)
app.include_router(v1_docs.router)
app.include_router(v1_assets.router)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_config().API_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],
)
exceptions.include_app(app)
Instrumentator().instrument(app).expose(app)


@app.get("/health", include_in_schema=False)
def health():
    return "ok"


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")
