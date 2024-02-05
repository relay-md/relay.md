# -*- coding: utf-8 -*-
from typing import List

from fastapi import Depends

from ...database import Session, get_session
from ...models.user import User
from ...repos.team import TeamRepo
from ...schema import (
    Response,
    TeamResponse,
)
from . import (
    require_authenticated_user,
    router,
)


@router.get(
    "/teams",
    tags=["v1"],
    response_model=Response[List[TeamResponse]],
)
async def get_docs(
    type: str = "all",
    page: int = 0,
    size: int = 50,
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)
    if type == "joined":
        teams = team_repo.joined(user, size, page)
    else:
        teams = team_repo.paginate(size, page)
    return dict(result=teams)
