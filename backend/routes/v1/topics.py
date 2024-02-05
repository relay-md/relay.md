# -*- coding: utf-8 -*-
from typing import List

from fastapi import Depends

from ...database import Session, get_session
from ...models.user import User
from ...repos.team_topic import TeamTopicRepo
from ...schema import Response, TeamTopicResponse, TeamTopicResponse
from . import (
    require_authenticated_user,
    router,
)


@router.get(
    "/topics",
    tags=["v1"],
    response_model=Response[List[TeamTopicResponse]],
)
async def get_docs(
    page: int = 0,
    size: int = 50,
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    team_topic_repo = TeamTopicRepo(db)
    team_topics = team_topic_repo.subscribed(user, size, page)
    return dict(result=team_topics)
