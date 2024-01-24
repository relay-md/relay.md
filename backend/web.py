# -*- coding: utf-8 -*-
import os

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.sessions import SessionMiddleware

from . import exceptions
from .config import get_config
from .database import Base, engine
from .routes import (
    admin,
    billing,
    contact,
    document,
    home,
    login,
    sitemap,
    stripe,
    subscribe,
    team,
    teams,
    topic,
)
from .routes.login import github, google

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
app.include_router(admin.router)
app.include_router(sitemap.router)

# TODO:
# exception handling:
#  * from authlib.integrations.starlette_client import  OAuthError
#
exceptions.include_app_web(app)
Instrumentator().instrument(app).expose(app)


@app.get("/health")
def health():
    return "ok"


@app.get(
    "/robots.txt",
    response_class=PlainTextResponse,
)
async def robotstxt():
    return """User-Agent: *
# Disallow: /document/
Disallow: /static/js/*.js
Disallow: /static/css/*.css
#
Sitenmap: https://relay.md/sitemap.xml
"""


# after the `app` variable
@app.middleware("http")
async def prerender(request: Request, call_next):
    user_agent = request.headers.get("user-agent", "").lower()
    request.state.is_prerender = False
    if ".xml" not in request.url.path:
        if "prerender" in user_agent:
            request.state.is_prerender = True
        else:
            if any([x in user_agent for x in get_config().PRERENDER_USER_AGENTS]):
                return RedirectResponse(
                    f"{get_config().PRERENDER_REDIRECT}{str(request.url)}"
                )
    response = await call_next(request)
    return response
