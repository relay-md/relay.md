# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Request

from ..config import Settings, get_config
from ..database import Session, get_session
from ..models.permissions import Permissions
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
    teams = team_repo.list_with_count_members()
    return templates.TemplateResponse(
        "teams.pug", context=dict(**locals(), Permissions=Permissions)
    )
