# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import JSONResponse

from .. import exceptions
from ..database import Session, get_session
from ..models.permissions import Permissions
from ..repos.team import Team
from ..repos.team_topic import TeamTopicRepo
from ..repos.user import UserRepo
from ..repos.user_team_topic import UserTeamTopicRepo
from ..utils.team import get_team, get_team_topic
from ..utils.user import User, require_user

router = APIRouter(prefix="/topic")


@router.post("/{team_topic_name}/subscribe")
async def subscribe(
    team_topic_name: str,
    request: Request,
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_team_topic_repo = UserTeamTopicRepo(db)
    user_repo = UserRepo(db)
    membership = user_repo.is_member(user, team_topic.team)
    # TODO: maybe we should introduce another permission here
    if not team_topic.team.can(Permissions.can_read, user, membership):
        return "not allowed"
    user_team_topic_repo.create_from_kwargs(
        user_id=user.id, team_topic_id=team_topic.id
    )
    response = JSONResponse(dict(status="ok"))
    response.headers["HX-Trigger"] = "refresh-topics"
    return response


@router.post("/{team_topic_name}/unsubscribe")
async def unsubscribe(
    team_topic_name: str,
    request: Request,
    team_topic: Team = Depends(get_team_topic),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_team_repo = UserTeamTopicRepo(db)
    user_team_topic = user_team_repo.get_by_kwargs(
        user_id=user.id, team_topic_id=team_topic.id
    )
    user_team_repo.delete(user_team_topic)
    response = JSONResponse(dict(status="ok"))
    response.headers["HX-Trigger"] = "refresh-topics"
    return response


@router.get("/{team_name}/api/topic/list")
async def api_list_topics_in_team(
    request: Request,
    search: str = Query(""),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    user_repo = UserRepo(db)
    topics = user_repo.get_subscriptions(user=user, team=team)
    ret = list()
    for topic_with_subscription in topics:
        topic = topic_with_subscription[0]
        if search and search not in topic.name:
            continue
        subscribed = topic_with_subscription[1]
        if subscribed:
            toggle_link = request.url_for("unsubscribe", team_topic_name=topic.name)
        else:
            toggle_link = request.url_for("subscribe", team_topic_name=topic.name)
        ret.append(
            dict(
                name=topic.name,
                id=topic.id,
                subscribed=subscribed,
                toggle_url=str(toggle_link),
            )
        )
    return ret


@router.post("/{team_name}/topic/create")
async def create_topic_htx(
    topic: str = Form(default=False),
    team: Team = Depends(get_team),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    if not team.user_id == user.id:
        return """<p id="validate-team-name" class="help is-danger">You cannot update the headline!</p>"""
    team_topic_repo = TeamTopicRepo(db)
    user_team_topic_repo = UserTeamTopicRepo(db)
    try:
        team_topic = team_topic_repo.from_string(f"{topic}@{team.name}", user)
        response = JSONResponse(dict(status="ok"))
        try:
            user_team_topic_repo.create_from_kwargs(
                user_id=user.id, team_topic_id=team_topic.id
            )
        except Exception:
            pass
    except exceptions.BaseAPIException as exc:
        response = JSONResponse(dict(error=str(exc)))
    response.headers["HX-Trigger"] = "refresh-topics"
    return response
