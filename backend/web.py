# -*- coding: utf-8 -*-
import os

from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from . import exceptions
from .config import config
from .database import Base, engine
from .routes import home, login, subscribe

# Create all tables
Base.metadata.create_all(engine)

app = FastAPI(openapi_url=None)
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
    ),
    name="static",
)

app.include_router(home.router)
app.include_router(login.router)
app.include_router(subscribe.router)

# TODO:
# exception handling:
#  * from authlib.integrations.starlette_client import  OAuthError
#
exceptions.include_app_web(app)

oauth = OAuth()
oauth.register(
    name="github",
    client_id=config.GITHUB_CLIENT_ID,
    client_secret=config.GITHUB_CLIENT_SECRET,
    client_kwargs={"scope": "read:user"},
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
)
