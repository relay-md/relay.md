# -*- coding: utf-8 -*-


from fastapi import Depends

from .. import exceptions
from ..database import Session, get_session
from ..repos.team import Team, TeamRepo
from ..repos.team_topic import TeamTopicRepo
from ..utils.user import User, get_optional_user


async def get_team(team_name: str, db: Session = Depends(get_session)) -> Team:
    team_repo = TeamRepo(db)
    team = team_repo.get_by_kwargs(name=team_name)
    if not team:
        raise exceptions.NotFound("team id unknown")
    return team


async def get_team_topic(
    team_topic_name: str,
    db: Session = Depends(get_session),
    user: User = Depends(get_optional_user),
):
    team_topic_repo = TeamTopicRepo(db)
    return team_topic_repo.from_string(team_topic_name, user)
