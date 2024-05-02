# -*- coding: utf-8 -*-

from uuid import UUID

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse

from .. import exceptions
from ..config import Settings, get_config
from ..database import Session, get_session
from ..models.permissions import Permissions
from ..repos.team import Team, TeamRepo
from ..repos.user import UserRepo
from ..repos.user_team import UserTeamRepo
from ..templates import templates
from ..utils.team import get_team
from ..utils.user import User, get_optional_user, require_user

router = APIRouter(prefix="/team")


@router.get("/{team_name}")
async def show_team(
    team_name: str,
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_repo = UserRepo(db)
    membership = user_repo.is_member(user, team)
    return templates.TemplateResponse(
        "team.pug", context=dict(**locals(), Permissions=Permissions)
    )


@router.get("/{team_name}/join")
async def join(
    team_name: str,
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_team_repo = UserTeamRepo(db)
    if not team.can(Permissions.can_join, user):
        raise exceptions.NotAllowed(f"You are not allowed to join team {team_name}!")
    user_team_repo.add_member(user=user, team=team)
    return RedirectResponse(url=request.url_for("show_team", team_name=team_name))


@router.get("/{team_name}/leave")
async def leave(
    team_name: str,
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = UserTeamRepo(db)
    user_team = repo.get_by_kwargs(user_id=user.id, team_id=team.id)
    repo.remove_member(user_team)
    return RedirectResponse(url=request.url_for("show_team", team_name=team_name))


@router.get("/{team_name}/invite/{user_id}")
async def invite_user(
    team_name: str,
    user_id: UUID,
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_repo = UserRepo(db)
    new_user = user_repo.get_by_kwargs(id=user_id)
    if not new_user:
        raise exceptions.BadRequest("Invalid user id!")
    membership = user_repo.is_member(user, team)
    if not team.can(Permissions.can_invite, user, membership):
        raise exceptions.NotAllowed(
            f"You are not allowed to invite to team {team_name}!"
        )
    user_team_repo = UserTeamRepo(db)
    # only add if not already added
    if not user_team_repo.get_by_kwargs(user_id=new_user.id, team_id=team.id):
        user_team_repo.add_member(user=new_user, team=team)
    return RedirectResponse(url=request.url_for("settings", team_name=team_name))


@router.get("/{team_name}/remove/{membership_id}")
async def remove_user(
    team_name: str,
    membership_id: UUID,
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_repo = UserRepo(db)
    user_team_repo = UserTeamRepo(db)
    membership_to_remove = user_team_repo.get_by_kwargs(id=membership_id)
    if not membership_to_remove:
        raise exceptions.BadRequest("Invalid membership id!")
    membership = user_repo.is_member(user, team)
    # TODO: can invite means -> can remove from team, too!
    if not team.can(Permissions.can_invite, user, membership):
        raise exceptions.NotAllowed(
            f"You are not allowed to invite to team {team_name}!"
        )
    user_team_repo.remove_member(membership_to_remove)
    return RedirectResponse(url=request.url_for("settings", team_name=team_name))


@router.get("/{team_name}/toggle/perm")
async def toggle_team_perms(
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
    type: str = Query(default=""),
    perm: int = Query(default=0),
):
    if team.user_id != user.id:
        raise exceptions.NotAllowed(f"Team {team.name} is not your team!")
    if not type:
        raise exceptions.BadRequest("Need a 'type'!")
    team_repo = TeamRepo(db)
    if type == "owner":
        team_repo.update(
            team, owner_permissions=(team.owner_permissions ^ Permissions(perm)).value
        )
    elif type == "member":
        team_repo.update(
            team, member_permissions=(team.member_permissions ^ Permissions(perm)).value
        )
    elif type == "public":
        # Changing this flag requries upgrade
        new_perm = team.public_permissions ^ Permissions(perm)
        team_repo.update(team, public_permissions=(new_perm).value)
    else:
        raise exceptions.BadRequest(f"Invalid value for {type=}")
    return RedirectResponse(url=request.url_for("settings", team_name=team.name))


@router.get("/{team_name}/toggle/perm/member")
async def toggle_member_perms(
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
    member_id: UUID = Query(default=None),
    perm: int = Query(default=None),
):
    if team.user_id != user.id:
        raise exceptions.NotAllowed(f"Team {team.name} is not your team!")
    user_team_repo = UserTeamRepo(db)
    membership = user_team_repo.get_by_id(member_id)
    if not membership:
        raise exceptions.BadRequest("Member not found")
    if perm:
        new_perms = (membership.permissions or team.member_permissions) ^ Permissions(
            perm
        )
        user_team_repo.update(
            membership,
            permissions=new_perms.value,
        )
    else:
        user_team_repo.update(membership, permissions=0)
    return RedirectResponse(url=request.url_for("settings", team_name=team.name))


@router.get("/{team_name}/settings")
async def settings(
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
    size: int = Query(default=10),
    page: int = Query(default=0),
):
    team_repo = TeamRepo(db)
    members = team_repo.list_team_members(team, page, size)
    return templates.TemplateResponse(
        "team-admin.pug", context=dict(**locals(), Permissions=Permissions)
    )


@router.post("/{team_name}/settings/user/search", response_class=PlainTextResponse)
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

    def user_invite_link(user, team):
        return f"""
            <a href="{request.url_for("invite_user", team_name=team_name, user_id=user.id)}" class="list-item">
             <div class="list-item-image">
              <figure class="image is-32x32">
               <img class="is-rounded" src="{user.profile_picture_url}" />
              </figure>
             </div>
             <div class="list-item-content">
              <div class="list-item-title">
               @{user.username}
              </div>
              <div class="list-item-description">
               {user.name}
              </div>
             </div>
            </a>
        """

    ret = "\n".join([user_invite_link(x, team) for x in users])
    return f"""
        <div class="list">
        {ret}
        </div>
    """


@router.post("/new/validate-team-name", response_class=PlainTextResponse)
async def team_create_validate_team_name(
    request: Request,
    team_name: str = Form(default=""),
    user: User = Depends(get_optional_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)
    if team_repo.team_name_search(team_name.lower()):
        return """<p id="validate-team-name" class="help is-danger">A Team with this name already exists!</p>"""
    if not Team.validate_team_name(team_name):
        return """<p id="validate-team-name" class="help is-danger">The team name is invalid! Alphanumeric names only (a-z, 0-9 and _)</p>"""
    else:
        return ""


@router.post("/{team_name}/headline", response_class=PlainTextResponse)
async def update_team_headline(
    request: Request,
    headline: str = Form(default=""),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)
    if not team.user_id == user.id:
        return """<p id="validate-team-name" class="help is-danger">You cannot update the headline!</p>"""
    if len(headline) > 63:
        return (
            """<p id="validate-team-name" class="help is-danger">Max length 63!</p>"""
        )
    team_repo.update(team, headline=headline)
    return (
        """<p id="validate-team-name" class="help is-success">Headline updated!</p>"""
    )


@router.post("/{team_name}/description", response_class=PlainTextResponse)
async def update_team_description(
    request: Request,
    description: str = Form(default=""),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)
    if not team.user_id == user.id:
        return """<p id="validate-team-name" class="help is-danger">You cannot update the description!</p>"""
    if len(description) > 63:
        return (
            """<p id="validate-team-name" class="help is-danger">Max length 63!</p>"""
        )
    team_repo.update(team, description=description)
    return """<p id="validate-team-name" class="help is-success">description updated!</p>"""


@router.post("/{team_name}/toggle/hide", response_class=PlainTextResponse)
async def update_team_hide(
    request: Request,
    hide: bool = Form(default=False),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)
    if not team.user_id == user.id:
        return """<p id="validate-team-name" class="help is-danger">You cannot update the headline!</p>"""
    team_repo.update(team, hide=hide)
    return """<p id="validate-team-name" class="help is-success">Team updated!</p>"""


@router.post("/{team_name}/seats", response_class=PlainTextResponse)
async def update_team_seats(
    request: Request,
    seats: int = Form(default=0),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    raise NotImplementedError("This endpoint is unavailable in open source version")


@router.get("/{team_name}/billing")
async def team_billing(
    request: Request,
    team_name: str,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    raise NotImplementedError("This endpoint is unavailable in open source version")


@router.get("/{team_name}/billing/subscription/cancel")
async def cancel_subscription(
    request: Request,
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    raise NotImplementedError("This endpoint is unavailable in open source version")
