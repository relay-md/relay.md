# -*- coding: utf-8 -*-
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from .config import config
from .database import Base, engine
from .routes import home, login

# Create all tables
Base.metadata.create_all(engine)

app = FastAPI(openapi_url=None)
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

app.include_router(home.router)
app.include_router(login.router)

# TODO:
# exception handling:
#  * from authlib.integrations.starlette_client import  OAuthError
