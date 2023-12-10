# -*- coding: utf-8 -*-

from uuid import UUID

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse

from .. import exceptions
from ..config import Settings, get_config
from ..database import Session, get_session
from ..models.team import TeamType
from ..repos.team import Team, TeamRepo
from ..repos.team_topic import TeamTopicRepo
from ..repos.user import UserRepo
from ..repos.user_team import UserTeamRepo
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
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    user_repo = UserRepo(db)
    team_repo = TeamRepo(db)
    teams = team_repo.list()
    return templates.TemplateResponse("teams.pug", context=dict(**locals()))


@router.get("/topic/{team_topic_name}/subscribe")
async def subscribe(
    team_topic_name: str,
    request: Request,
    config: Settings = Depends(get_config),
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = UserTeamTopicRepo(db)
    if team_topic.team.is_private:
        raise exceptions.NotAllowed(f"Team {team_topic.team.name} is private!")
    repo.create_from_kwargs(user_id=user.id, team_topic_id=team_topic.id)
    return RedirectResponse(url=request.url_for("get_teams"))


@router.get("/topic/{team_topic_name}/unsubscribe")
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
    return RedirectResponse(url=request.url_for("get_teams"))


@router.get("/team/{team_name}/join")
async def join(
    team_name: str,
    request: Request,
    config: Settings = Depends(get_config),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = UserTeamRepo(db)
    if team.is_private or team.is_restricted:
        raise exceptions.NotAllowed(f"Team {team.name} is private or restricted!")
    repo.create_from_kwargs(user_id=user.id, team_id=team.id)
    return RedirectResponse(url=request.url_for("get_teams"))


@router.get("/team/{team_name}/invite/{user_id}")
async def invite_user(
    team_name: str,
    user_id: UUID,
    request: Request,
    config: Settings = Depends(get_config),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    if team.is_public:
        raise exceptions.NotAllowed("No need to invite anyone to a public team!")

    user_repo = UserRepo(db)
    new_user = user_repo.get_by_kwargs(id=user_id)
    if not new_user:
        raise exceptions.BadRequest("Invalid user id!")
    membership = user_repo.is_member(user, team)
    user_team_repo = UserTeamRepo(db)
    if (team.is_private or team.is_restricted) and not membership:
        # TODO: check that we are allowed to invite people
        raise exceptions.NotAllowed(
            f"Team {team.name} is private or restricted and you are not member!"
        )

    if not membership.can_invite_users:
        raise exceptions.NotAllowed(
            f"You are not allowed to invite to team {team_name}!"
        )
    user_team_repo.create_from_kwargs(user_id=new_user.id, team_id=team.id)
    return RedirectResponse(url=request.url_for("settings", team_name=team_name))


@router.get("/team/{team_name}/remove/{membership_id}")
async def remove_user(
    team_name: str,
    membership_id: UUID,
    request: Request,
    config: Settings = Depends(get_config),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    if team.is_public:
        raise exceptions.NotAllowed("You cannot uninvite anyone from global teams!")
    user_repo = UserRepo(db)
    user_team_repo = UserTeamRepo(db)
    membership_to_remove = user_team_repo.get_by_kwargs(id=membership_id)
    if not membership_to_remove:
        raise exceptions.BadRequest("Invalid membership id!")
    membership = user_repo.is_member(user, team)
    if (team.is_private or team.is_restricted) and not membership:
        # TODO: check that we are allowed to invite people
        raise exceptions.NotAllowed(
            f"Team {team.name} is private or restricted and you are not member!"
        )

    if not membership.can_invite_users:
        raise exceptions.NotAllowed(
            f"You are not allowed to manage members of team {team_name}!"
        )
    user_team_repo.delete(membership_to_remove)
    return RedirectResponse(url=request.url_for("settings", team_name=team_name))


@router.get("/team/{team_name}/leave")
async def leave(
    team_name: str,
    request: Request,
    config: Settings = Depends(get_config),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = UserTeamRepo(db)
    user_team = repo.get_by_kwargs(user_id=user.id, team_id=team.id)
    repo.delete(user_team)
    return RedirectResponse(url=request.url_for("get_teams"))


@router.get("/team/{team_name}/settings")
async def settings(
    request: Request,
    config: Settings = Depends(get_config),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
    size: int = Query(default=10),
    page: int = Query(default=0),
):
    team_repo = TeamRepo(db)
    members = team_repo.list_team_members(team, page, size)
    return templates.TemplateResponse("team-admin.pug", context=dict(**locals()))


@router.post("/team/{team_name}/settings/type", response_class=PlainTextResponse)
async def settings_type_post(
    request: Request,
    type: str = Form(default=""),
    config: Settings = Depends(get_config),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)
    team_repo.update(team, type=TeamType(type))
    return """
        <div class="notification is-success is-light">
        Change saved successfully
        </div>
    """


@router.post("/team/{team_name}/settings/user/search", response_class=PlainTextResponse)
async def settings_user_search(
    request: Request,
    team_name: str,
    config: Settings = Depends(get_config),
    name: str = Form(default=""),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    if len(name) < 3:
        return
    user_repo = UserRepo(db)
    users = list(user_repo.search_username(name, limit=5))

    def user_invite_link(user):
        return f"""
            <a href="{request.url_for("invite_user", team_name=team_name, user_id=user.id)}" class="list-item">
            <span class="icon-text"><span class="icon"><i class="fab fa-{user.oauth_provider.value}"></i></span><span>{user.username}</span></a>
        """

    ret = "\n".join([user_invite_link(x) for x in users])
    return f"""
        <div class="list">
        {ret}
        </div>
    """
