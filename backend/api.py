# -*- coding: utf-8 -*-
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .config import config
from .database import Base, engine
from .routes import api, v0

# Create all tables
Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(v0.router)
# app.include_router(api.router)
assert api.router

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.API_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],
)

# TODO:
# exception handling:
#  * from authlib.integrations.starlette_client import  OAuthError
