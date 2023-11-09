# -*- coding: utf-8 -*-
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

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

# TODO:
# exception handling:
#  * from authlib.integrations.starlette_client import  OAuthError
