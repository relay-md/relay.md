# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from .. import exceptions
from ..config import Settings, get_config
from ..database import Session, get_session
from ..repos.team import Team
from ..repos.user_team_topic import UserTeamTopicRepo
from ..utils.team import get_team_topic
from ..utils.user import User, require_user

router = APIRouter(prefix="/topic")


@router.get("/{team_topic_name}/subscribe")
async def subscribe(
    team_topic_name: str,
    request: Request,
    config: Settings = Depends(get_config),
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = UserTeamTopicRepo(db)
    # TODO: this needs updating!!
    if team_topic.team.is_private:
        raise exceptions.NotAllowed(f"Team {team_topic.team.name} is private!")
    repo.create_from_kwargs(user_id=user.id, team_topic_id=team_topic.id)
    return RedirectResponse(
        url=request.url_for("show_team", team_name=team_topic.team.name)
    )


@router.get("/{team_topic_name}/unsubscribe")
async def unsubscribe(
    team_topic_name: str,
    request: Request,
    config: Settings = Depends(get_config),
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = UserTeamTopicRepo(db)
    user_team_topic = repo.get_by_kwargs(user_id=user.id, team_topic_id=team_topic.id)
    repo.delete(user_team_topic)
    return RedirectResponse(
        url=request.url_for("show_team", team_name=team_topic.team.name)
    )
