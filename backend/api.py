# -*- coding: utf-8 -*-
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from . import exceptions
from .config import get_config
from .database import Base, engine
from .routes import v1

# Create all tables
Base.metadata.create_all(engine)

# Load metadata from yaml file
app = FastAPI(**get_config().FASTAPI_CONFIG)
app.include_router(v1.router)

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
