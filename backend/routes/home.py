# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse

from ..repos.user import User
from ..templates import templates
from ..utils.user import get_optional_user

router = APIRouter(prefix="")


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=["web"],
)
async def welcome(request: Request, user: User = Depends(get_optional_user)):
    return templates.TemplateResponse("welcome.html", context=dict(**locals()))
