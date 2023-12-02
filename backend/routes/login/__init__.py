# -*- coding: utf-8 -*-
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

router = APIRouter(prefix="")
oauth = OAuth()


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    request.session.pop("user_id", None)
    request.session.pop("access_token", None)
    return RedirectResponse(url="/")


@router.get("/register")
async def register(request: Request, next: Optional[str] = ""):
    return RedirectResponse(url="/login/github")


# TODO: Deal with the next-url item below, maybe build a stack of urls to visit
# in a session like in previous projects
@router.get("/login")
async def login(request: Request, next: Optional[str] = ""):
    return RedirectResponse(url="/login/github")
