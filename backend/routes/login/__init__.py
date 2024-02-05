# -*- coding: utf-8 -*-
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse

from ...config import Settings, get_config
from ...database import Session, get_session
from ...repos.user import User, UserRepo
from ...templates import templates
from ...utils.url import add_next_url, get_next_url
from ...utils.user import get_optional_user, require_user

router = APIRouter(prefix="")
oauth = OAuth()


@router.get("/stack")
async def satck(request: Request, next: Optional[str] = None):
    add_next_url(request, next)
    return request.session["next"]


@router.get("/logout")
async def logout(request: Request, next: Optional[str] = None):
    add_next_url(request, next)
    request.session.pop("user", None)
    request.session.pop("user_id", None)
    request.session.pop("access_token", None)
    return RedirectResponse(url=get_next_url(request) or "/")


@router.get("/register")
async def register(
    request: Request,
    next: Optional[str] = None,
    config: Settings = Depends(get_config),
    user: User = Depends(get_optional_user),
):
    if user:
        return RedirectResponse(url="/")
    add_next_url(request, next)
    return templates.TemplateResponse("login.pug", context=locals())


# TODO: Deal with the next-url item below, maybe build a stack of urls to visit
# in a session like in previous projects
@router.get("/login")
async def login(
    request: Request,
    next: Optional[str] = None,
    config: Settings = Depends(get_config),
    user: User = Depends(get_optional_user),
):
    if user:
        return RedirectResponse(url="/")
    add_next_url(request, next)
    return templates.TemplateResponse("login.pug", context=locals())


@router.get("/configure/obsidian")
async def configure_obsidian(
    request: Request,
    user: User = Depends(require_user),
    config: Settings = Depends(get_config),
):
    access_token = request.session["access_token"]
    return RedirectResponse(
        url=f"obsidian://relay.md:access-token?token={access_token}&username={user.username}&api_url={config.API_URI}"
    )


@router.post("/onboarding/check-username", response_class=PlainTextResponse)
async def onboarding_check_username(
    request: Request,
    username: str = Form(default=""),
    db: Session = Depends(get_session),
):
    user_repo = UserRepo(db)
    if user_repo.get_by_kwargs(username=username):
        return "<span class='help is-danger'>User exists</span><script>invalidUsername();</script>"
    return "<script>validUsername();</script>"
