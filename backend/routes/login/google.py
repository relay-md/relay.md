# -*- coding: utf-8 -*-
import json
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, status
from starlette.responses import RedirectResponse

from ...config import Settings, get_config
from ...database import Session, get_session
from ...models.user import OauthProvider
from ...repos.access_token import AccessTokenRepo
from ...repos.user import UserRepo
from ...templates import templates
from ...utils.url import get_next_url
from . import oauth

router = APIRouter(prefix="/login/google")
oauth.register(
    name="google",
    client_id=get_config().GOOGLE_CLIENT_ID,
    client_secret=get_config().GOOGLE_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    },
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
    user_repo = UserRepo(db)
    access_token_repo = AccessTokenRepo(db)
    user = user_repo.get_by_kwargs(
        email=google_user["email"].lower(), oauth_provider=OauthProvider.GOOGLE
    )
    if not user:
        # Store token in session and head over to asking for a username
        request.session["token"] = json.dumps(token)
        return RedirectResponse(url=request.url_for("onboarding_google"))

    access_token = access_token_repo.get_by_kwargs(user_id=user.id)
    if not access_token:
        access_token = access_token_repo.create_from_kwargs(user_id=user.id)
    request.session["user_id"] = str(user.id)
    request.session["access_token"] = str(access_token.token)
    return RedirectResponse(url=get_next_url(request) or "/")


@router.get("/onboarding")
async def onboarding_google(request: Request, config: Settings = Depends(get_config)):
    return templates.TemplateResponse("google-onboarding.pug", context=locals())


@router.post("/onboarding")
async def onboarding_google_post(
    request: Request,
    username: str = Form(default=""),
    db: Session = Depends(get_session),
):
    token = request.session.get("token")
    if not token:
        return RedirectResponse(url=get_next_url(request) or "/")
    token = json.loads(token)
    google_user = token.get("userinfo")
    user_repo = UserRepo(db)
    access_token_repo = AccessTokenRepo(db)
    user = user_repo.create_from_kwargs(
        username=username,
        email=google_user["email"].lower(),
        name=google_user["name"].lower(),
        profile_picture_url=google_user["picture"],
        oauth_provider=OauthProvider.GOOGLE,
    )
    access_token = access_token_repo.get_by_kwargs(user_id=user.id)
    if not access_token:
        access_token = access_token_repo.create_from_kwargs(user_id=user.id)
    request.session["user_id"] = str(user.id)
    request.session["access_token"] = str(access_token.token)
    # Remove token from session, we don't need it anymore
    request.session.pop("token")
    return RedirectResponse(
        url=get_next_url(request) or "/", status_code=status.HTTP_302_FOUND
    )
