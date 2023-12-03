# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from .. import exceptions
from ..config import config
from ..database import Session, get_session
from ..repos.team import Team, TeamRepo
from ..repos.team_topic import TeamTopicRepo
from ..repos.user import UserRepo
from ..repos.user_team_topic import UserTeamTopicRepo
from ..templates import templates
from ..utils.user import User, require_user

router = APIRouter(prefix="")


async def get_team(team_name: str, db: Session = Depends(get_session)) -> Team:
    team_repo = TeamRepo(db)
    team = team_repo.get_by_kwargs(name=team_name)
    if not team:
        raise exceptions.NotFound("team id unknown")
    return team


async def get_team_topic(team_topic_name: str, db: Session = Depends(get_session)):
    team_topic_repo = TeamTopicRepo(db)
    return team_topic_repo.from_string(team_topic_name)


@router.get("/teams")
async def get_teams(
    request: Request,
    config=config,
    db: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    user_repo = UserRepo(db)
    team_repo = TeamRepo(db)
    teams = team_repo.list(is_private=False)
    return templates.TemplateResponse("teams.pug", context=dict(**locals()))


@router.get("/{team_topic_name}/subscribe")
async def subscribe(
    team_topic_name: str,
    request: Request,
    config=config,
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = UserTeamTopicRepo(db)
    repo.create_from_kwargs(user_id=user.id, team_topic_id=team_topic.id)
    return RedirectResponse(url=request.url_for("get_teams"))


@router.get("/{team_topic_name}/unsubscribe")
async def unsubscribe(
    team_topic_name: str,
    request: Request,
    config=config,
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = UserTeamTopicRepo(db)
    user_team_topic = repo.get_by_kwargs(user_id=user.id, team_topic_id=team_topic.id)
    if user_team_topic:
        repo.delete(user_team_topic)
    return RedirectResponse(url=request.url_for("get_teams"))
