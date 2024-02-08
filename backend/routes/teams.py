# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse

from ..database import Session, get_session
from ..exceptions import BadRequest
from ..models.permissions import Permissions
from ..repos.team import TeamRepo
from ..repos.user import UserRepo
from ..templates import templates
from ..utils.user import User, get_optional_user, require_user

router = APIRouter(prefix="/teams")


@router.get("")
async def get_teams(
    request: Request,
    db: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    user_repo = UserRepo(db)
    team_repo = TeamRepo(db)
    teams = team_repo.list_selected_teams(user)
    return templates.TemplateResponse(
        "teams.pug", context=dict(**locals(), Permissions=Permissions)
    )


@router.post(
    "/search",
    response_class=PlainTextResponse,
)
async def search_team(
    request: Request,
    name: str = Form(""),
    db: Session = Depends(get_session),
    user: User = Depends(get_optional_user),
):
    team_repo = TeamRepo(db)
    if len(name) < 3:
        teams = team_repo.list_selected_teams(user)
    else:
        teams = team_repo.search_with_count(name)
    return templates.TemplateResponse(
        "teams-iterator.pug", context=dict(**locals(), Permissions=Permissions)
    )


@router.get(
    "/create",
    response_class=PlainTextResponse,
)
async def create_team(
    request: Request,
    db: Session = Depends(get_session),
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse(
        "team-create.pug", context=dict(**locals(), Permissions=Permissions)
    )


@router.post(
    "/create",
    response_class=PlainTextResponse,
)
async def create_team_post(
    request: Request,
    team_name: str = Form(""),
    db: Session = Depends(get_session),
    user: User = Depends(get_optional_user),
):
    team_repo = TeamRepo(db)
    team_name = team_name.lower()

    # check if team exists owned by user
    team = team_repo.get_by_kwargs(name=team_name)
    if team and team.user_id != user.id:
        raise BadRequest("This team exists already and it is not yours!")

    team_repo.create_from_kwargs(name=team_name, user_id=user.id)
    return RedirectResponse(
        url=request.url_for("show_team", team_name=team_name),
        status_code=status.HTTP_302_FOUND,
    )
