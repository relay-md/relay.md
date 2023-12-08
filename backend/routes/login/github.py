# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from ...config import config
from ...database import Session, get_session
from ...exceptions import BadRequest, NotAllowed
from ...models.user import OauthProvider
from ...repos.access_token import AccessTokenRepo
from ...repos.team_topic import TeamTopicRepo
from ...repos.user import UserRepo
from ...repos.user_team_topic import UserTeamTopicRepo
from ...utils.url import get_next_url
from . import oauth

router = APIRouter(prefix="/login/github")
oauth.register(
    name="github",
    client_id=config.GITHUB_CLIENT_ID,
    client_secret=config.GITHUB_CLIENT_SECRET,
    client_kwargs={"scope": "read:user"},
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
)


@router.get("")
async def login_github(request: Request, next: Optional[str] = ""):
    redirect_uri = request.url_for("auth_github")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth_github(request: Request, db: Session = Depends(get_session)):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)
    github_user = resp.json()
    user_repo = UserRepo(db)
    access_token_repo = AccessTokenRepo(db)
    user = user_repo.get_by_kwargs(
        username=github_user["login"].lower(), oauth_provider=OauthProvider.GITHUB
    )
    if not user:
        user = user_repo.create_from_kwargs(
            username=github_user["login"].lower(),
            email=github_user["email"].lower(),
            name=github_user["name"].lower(),
            location=github_user["location"],
            oauth_provider=OauthProvider.GITHUB,
        )

        # Automatically subscribe to some team topics
        team_topic_repo = TeamTopicRepo(db)
        user_team_topic_repo = UserTeamTopicRepo(db)
        for subscribe_to in config.NEW_USER_SUBSCRIBE_TO:
            try:
                team_topic = team_topic_repo.from_string(subscribe_to)
                user_team_topic_repo.create_from_kwargs(
                    user_id=user.id, team_topic_id=team_topic.id
                )
            except (BadRequest, NotAllowed):
                # may fail if the team topic does not exist
                # or creation of topic is not allowed
                pass

    access_token = access_token_repo.get_by_kwargs(user_id=user.id)
    if not access_token:
        access_token = access_token_repo.create_from_kwargs(user_id=user.id)
    if github_user:
        request.session["user_id"] = str(user.id)
        request.session["access_token"] = str(access_token.token)
    return RedirectResponse(url=get_next_url(request) or "/")
