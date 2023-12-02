# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse

from ..config import Settings, config
from ..repos.user import User
from ..templates import templates
from ..utils.user import get_optional_user

router = APIRouter(prefix="")


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=["web"],
)
async def welcome(
    request: Request, user: User = Depends(get_optional_user), config: Settings = config
):
    return templates.TemplateResponse("welcome.html", context=dict(**locals()))


@router.get(
    "/profile",
    response_class=HTMLResponse,
    tags=["web"],
)
async def profile(
    request: Request, user: User = Depends(get_optional_user), config: Settings = config
):
    return templates.TemplateResponse("profile.pug", context=dict(**locals()))


@router.get(
    "/documentation/plugins/obsidian",
    response_class=HTMLResponse,
    tags=["web"],
)
async def obsidian_plugin(
    request: Request, user: User = Depends(get_optional_user), config: Settings = config
):
    return templates.TemplateResponse("plugin.pug", context=dict(**locals()))


@router.get(
    "/documentation/relay/basics",
    response_class=HTMLResponse,
    tags=["web"],
)
async def relay_basics(
    request: Request, user: User = Depends(get_optional_user), config: Settings = config
):
    return templates.TemplateResponse("howto-relay.pug", context=dict(**locals()))
