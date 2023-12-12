# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Query, Request

from ..config import Settings, get_config
from ..database import Session, get_session
from ..repos.team import TeamRepo
from ..repos.user import UserRepo
from ..templates import templates
from ..utils.user import User, require_user

router = APIRouter(prefix="/teams")


@router.get("")
async def get_teams(
    request: Request,
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    user_repo = UserRepo(db)
    team_repo = TeamRepo(db)
    teams = team_repo.list()
    return templates.TemplateResponse("teams.pug", context=dict(**locals()))


@router.get("/new")
async def team_create(
    request: Request,
    type: str = Query(default="public"),
    yearly: bool = Query(default=False),
    config: Settings = Depends(get_config),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    print(type, yearly)
    return templates.TemplateResponse("pricing.pug", context=dict(**locals()))
