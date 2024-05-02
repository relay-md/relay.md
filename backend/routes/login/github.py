# -*- coding: utf-8 -*-
import json
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, status
from starlette.responses import RedirectResponse

from ...config import Settings, get_config
from ...database import Session, get_session
from ...exceptions import BadRequest, NotAllowed
from ...models.user import OauthProvider
from ...repos.access_token import AccessTokenRepo
from ...repos.newsletter import NewsletterRepo
from ...repos.team_topic import TeamTopicRepo
from ...repos.user import UserRepo
from ...repos.user_team_topic import UserTeamTopicRepo
from ...templates import templates
from ...utils.url import get_next_url
from . import oauth

router = APIRouter(prefix="/login/github")
oauth.register(
    name="github",
    client_id=get_config().GITHUB_CLIENT_ID,
    client_secret=get_config().GITHUB_CLIENT_SECRET,
    client_kwargs={"scope": "read:user user:email"},
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
    email = github_user.get("email")
    if not email:
        resp = await oauth.github.get("user/emails", token=token)
        emails = resp.json()
        email = next(filter(lambda x: x["primary"] is True, emails))
        email = email["email"]
    user_repo = UserRepo(db)
    access_token_repo = AccessTokenRepo(db)
    user = user_repo.get_by_kwargs(
        email=email.lower(), oauth_provider=OauthProvider.GITHUB
    )
    if not user:
        # Store token in session and head over to asking for a username
        request.session["token"] = json.dumps(token)
        return RedirectResponse(url=request.url_for("onboarding_github"))
    else:
        access_token = access_token_repo.get_by_kwargs(user_id=user.id)
    request.session["user_id"] = str(user.id)
    request.session["access_token"] = str(access_token.token)
    return RedirectResponse(url=get_next_url(request) or "/")


@router.get("/onboarding")
async def onboarding_github(request: Request, config: Settings = Depends(get_config)):
    return templates.TemplateResponse("github-onboarding.pug", context=locals())


@router.post("/onboarding")
async def onboarding_github_post(
    request: Request,
    username: str = Form(default=""),
    first_name: str = Form(default=""),
    last_name: str = Form(default=""),
    accept_tos: bool = Form(default=False),
    accept_privacy: bool = Form(default=False),
    accept_newsletter: bool = Form(default=False),
    join_news_team: bool = Form(default=False),
    db: Session = Depends(get_session),
):
    if not accept_tos or not accept_privacy:
        raise BadRequest("You need to accept tos and privacy policy!")
    token = request.session.get("token")
    if not token:
        return RedirectResponse(url=get_next_url(request) or "/")
    token = json.loads(token)
    resp = await oauth.github.get("user", token=token)
    github_user = resp.json()
    email = github_user.get("email")
    if not email:
        resp = await oauth.github.get("user/emails", token=token)
        emails = resp.json()
        email = next(filter(lambda x: x["primary"] is True, emails))
        email = email["email"]
    user_repo = UserRepo(db)
    user = user_repo.create_from_kwargs(
        username=username,
        email=email.lower(),
        firstname=first_name,
        lastname=last_name,
        name=f"{first_name} {last_name}",
        oauth_provider=OauthProvider.GITHUB,
        profile_picture_url=github_user["avatar_url"],
    )

    # Generate access token for the user session
    access_token_repo = AccessTokenRepo(db)
    access_token = access_token_repo.get_by_kwargs(user_id=user.id)
    if not access_token:
        access_token = access_token_repo.create_from_kwargs(user_id=user.id)

    # Accept newsletter
    if accept_newsletter:
        newsletter_repo = NewsletterRepo()
        try:
            newsletter_repo.subscribe(email, first_name, last_name, status="subscribed")
        except Exception:
            pass

    # Automatically subscribe to some team topics
    if join_news_team:
        team_topic_repo = TeamTopicRepo(db)
        user_team_topic_repo = UserTeamTopicRepo(db)
        for subscribe_to in get_config().NEW_USER_SUBSCRIBE_TO:
            try:
                team_topic = team_topic_repo.from_string(subscribe_to, user)
                user_team_topic_repo.create_from_kwargs(
                    user_id=user.id, team_topic_id=team_topic.id
                )
            except (BadRequest, NotAllowed):
                # may fail if the team topic does not exist
                # or creation of topic is not allowed
                pass

    # Store stuff in the user session
    request.session["user_id"] = str(user.id)
    request.session["access_token"] = str(access_token.token)

    # Remove token from session, we don't need it anymore
    request.session.pop("token")

    return RedirectResponse(
        url=get_next_url(request) or "/", status_code=status.HTTP_302_FOUND
    )
