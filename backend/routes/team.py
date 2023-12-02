# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Request

from ..config import config
from ..database import Session, get_session
from ..repos.team import TeamRepo
from ..templates import templates

router = APIRouter(prefix="")


@router.get("/teams")
async def get_teams(
    request: Request, config=config, db: Session = Depends(get_session)
):
    team_repo = TeamRepo(db)
    teams = team_repo.list(is_private=False)
    return templates.TemplateResponse("teams.pug", context=dict(**locals()))
