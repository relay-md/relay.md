# -*- coding: utf-8 -*-
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.sessions import SessionMiddleware

from . import exceptions
from .config import get_config
from .database import Base, engine
from .routes import (
    billing,
    contact,
    document,
    home,
    login,
    stripe,
    subscribe,
    team,
    teams,
    topic,
)
from .routes.login import github, google

# Create all tables
Base.metadata.create_all(engine)

app = FastAPI(openapi_url=None)
app.add_middleware(SessionMiddleware, secret_key=get_config().SECRET_KEY)

app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
    ),
    name="static",
)

app.include_router(home.router)
app.include_router(login.router)
app.include_router(github.router)
app.include_router(google.router)
app.include_router(subscribe.router)
app.include_router(document.router)
app.include_router(team.router)
app.include_router(teams.router)
app.include_router(topic.router)
app.include_router(billing.router)
app.include_router(stripe.router)
app.include_router(contact.router)

# TODO:
# exception handling:
#  * from authlib.integrations.starlette_client import  OAuthError
#
exceptions.include_app_web(app)
Instrumentator().instrument(app).expose(app)


@app.get("/health")
def health():
    return "ok"
