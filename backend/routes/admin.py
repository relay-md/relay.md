# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from ..config import Settings, get_config
from ..database import Session, get_session
from ..repos.team import TeamRepo
from ..utils.team import Team, get_team
from ..utils.user import User, require_admin

router = APIRouter(prefix="/admin")


@router.get("team/toggle_favorit/{team_name}")
async def toggle_team_favorit(
    request: Request,
    config: Settings = Depends(get_config),
    team: Team = Depends(get_team),
    db: Session = Depends(get_session),
    user: User = Depends(require_admin),
):
    team_repo = TeamRepo(db)
    team_repo.update(team, favorit=not team.favorit)
    return RedirectResponse(url=request.url_for("get_teams"))
