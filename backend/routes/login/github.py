# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from ...config import get_config
from ...database import Session, get_session
from ...models.user import OauthProvider
from ...repos.access_token import AccessTokenRepo
from ...repos.user import UserRepo
from ...utils.url import get_next_url
from . import oauth

router = APIRouter(prefix="/login/github")
oauth.register(
    name="github",
    client_id=get_config().GITHUB_CLIENT_ID,
    client_secret=get_config().GITHUB_CLIENT_SECRET,
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
            oauth_provider=OauthProvider.GITHUB,
            profile_picture_url=github_user["avatar_url"],
        )
        access_token = access_token_repo.create_from_kwargs(user_id=user.id)
    else:
        access_token = access_token_repo.get_by_kwargs(user_id=user.id)
    request.session["user_id"] = str(user.id)
    request.session["access_token"] = str(access_token.token)
    return RedirectResponse(url=get_next_url(request) or "/")
