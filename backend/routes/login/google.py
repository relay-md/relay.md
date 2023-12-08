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

router = APIRouter(prefix="/login/google")
oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)


@router.get("")
async def login_google(request: Request, next: Optional[str] = ""):
    redirect_uri = request.url_for("auth_google")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth_google(request: Request, db: Session = Depends(get_session)):
    token = await oauth.google.authorize_access_token(request)
    google_user = token.get("userinfo")
    print(google_user)
    user_repo = UserRepo(db)
    access_token_repo = AccessTokenRepo(db)
    user = user_repo.get_by_kwargs(
        username=google_user["name"].lower(), oauth_provider=OauthProvider.GOOGLE
    )
    if not user:
        user = user_repo.create_from_kwargs(
            # FIXME: MUST ASK USER TO PROVIDE A USERNAME!?!?
            username=google_user["sub"].lower(),
            email=google_user["email"].lower(),
            name=google_user["name"].lower(),
            location="",
            oauth_provider=OauthProvider.GOOGLE,
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
    if google_user:
        request.session["user_id"] = str(user.id)
        request.session["access_token"] = str(access_token.token)
    return RedirectResponse(url=get_next_url(request) or "/")
