# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import PlainTextResponse

from ..database import Session, get_session
from ..models.permissions import Permissions
from ..repos.team import TeamRepo
from ..repos.user import UserRepo
from ..templates import templates
from ..utils.user import User, get_optional_user, require_user

router = APIRouter(prefix="/teams")


@router.get("")
async def get_teams(
    request: Request,
    db: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    user_repo = UserRepo(db)
    team_repo = TeamRepo(db)
    teams = team_repo.list_selected_teams(user)
    return templates.TemplateResponse(
        "teams.pug", context=dict(**locals(), Permissions=Permissions)
    )


@router.post(
    "/search",
    response_class=PlainTextResponse,
)
async def search_team(
    request: Request,
    name: str = Form(""),
    db: Session = Depends(get_session),
    user: User = Depends(get_optional_user),
):
    team_repo = TeamRepo(db)
    if len(name) < 3:
        teams = team_repo.list_selected_teams(user)
    else:
        teams = team_repo.search_with_count(name)
    return templates.TemplateResponse(
        "teams-iterator.pug", context=dict(**locals(), Permissions=Permissions)
    )
