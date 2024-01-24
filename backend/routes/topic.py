# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from .. import exceptions
from ..database import Session, get_session
from ..models.permissions import Permissions
from ..repos.team import Team
from ..repos.user import UserRepo
from ..repos.user_team_topic import UserTeamTopicRepo
from ..utils.team import get_team_topic
from ..utils.user import User, require_user

router = APIRouter(prefix="/topic")


@router.get("/{team_topic_name}/subscribe")
async def subscribe(
    team_topic_name: str,
    request: Request,
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_team_repo = UserTeamTopicRepo(db)
    user_repo = UserRepo(db)
    membership = user_repo.is_member(user, team_topic.team)
    # TODO: maybe we should introduce another permission here
    if not team_topic.team.can(Permissions.can_read, user, membership):
        raise exceptions.NotAllowed(f"Team {team_topic.team.name} is private!")
    user_team_repo.create_from_kwargs(user_id=user.id, team_topic_id=team_topic.id)
    return RedirectResponse(
        url=request.url_for("show_team", team_name=team_topic.team.name)
    )


@router.get("/{team_topic_name}/unsubscribe")
async def unsubscribe(
    team_topic_name: str,
    request: Request,
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_team_repo = UserTeamTopicRepo(db)
    user_team_topic = user_team_repo.get_by_kwargs(
        user_id=user.id, team_topic_id=team_topic.id
    )
    user_team_repo.delete(user_team_topic)
    return RedirectResponse(
        url=request.url_for("show_team", team_name=team_topic.team.name)
    )
