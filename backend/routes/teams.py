# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import PlainTextResponse

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
    return templates.TemplateResponse("pricing.pug", context=dict(**locals()))


@router.post("/new/validate-team-name", response_class=PlainTextResponse)
async def team_create_validate_team_name(
    request: Request,
    team_name: str = Form(default=""),
    config: Settings = Depends(get_config),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)
    if team_repo.team_name_search(team_name.lower()):
        return """<p class="help is-danger">A Team with this name already exists!</p>"""
    else:
        return ""


@router.post("/billing")
async def team_billing_post(
    request: Request,
    config: Settings = Depends(get_config),
    type: str = Form(default="public"),
    yearly: bool = Form(default=False),
    team_name: str = Form(default=""),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    # FIXME: needs implemnetation
    return str([team_name, type, yearly])
