# -*- coding: utf-8 -*-
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .config import config
from .database import Base, engine
from .routes import api, home, login, v0

# Create all tables
Base.metadata.create_all(engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")
app.include_router(v0.router)

assert home.router
assert login.router
assert api.router

# app.include_router(home.router)
# app.include_router(login.router)
# app.include_router(api.router)
#
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
