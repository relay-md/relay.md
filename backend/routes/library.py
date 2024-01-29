# -*- coding: utf-8 -*-
import json
from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse

from ..database import get_session, Session
from ..repos.access_token import AccessTokenRepo
from ..repos.user import User
from ..templates import templates
from ..utils.user import get_optional_user

router = APIRouter(prefix="")


@router.get(
    "/team/{team_name}/library",
    response_class=HTMLResponse,
    tags=["web"],
)
async def library(
    team_name: str,
    request: Request,
    user: User = Depends(get_optional_user),
    db: Session = Depends(get_session),
):
    access_token = AccessTokenRepo(db).get_by_kwargs(user_id=user.id)
    auth_header = json.dumps({"x-api-key": str(access_token.token)})
    return templates.TemplateResponse("library.pug", context=dict(**locals()))
