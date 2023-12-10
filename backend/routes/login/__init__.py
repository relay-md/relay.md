# -*- coding: utf-8 -*-
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from ...config import Settings, get_config
from ...templates import templates
from ...utils.url import add_next_url, get_next_url
from ...utils.user import User, get_optional_user, require_user

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
async def configure_obsidian(request: Request, user: User = Depends(require_user)):
    access_token = request.session["access_token"]
    return RedirectResponse(
        url=f"obsidian://relay.md:access-token?token={access_token}"
    )
