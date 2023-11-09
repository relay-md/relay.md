import json
from rich import print
from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

from .routes import home, login, api, v0
from .database import Base, engine

# Create all tables
Base.metadata.create_all(engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")
app.include_router(v0.router)

assert (home.router)
assert (login.router)
assert (api.router)

#app.include_router(home.router)
#app.include_router(login.router)
#app.include_router(api.router)

# TODO:
# exception handling:
#  * from authlib.integrations.starlette_client import  OAuthError
