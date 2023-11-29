# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse

from .. import oauth
from ..database import Session, get_session
from ..models.user import OauthProvider
from ..repos.access_token import AccessTokenRepo
from ..repos.user import UserRepo

router = APIRouter(prefix="")


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    request.session.pop("user_id", None)
    request.session.pop("access_token", None)
    return RedirectResponse(url="/")


@router.get("/register")
async def register(request: Request):
    return RedirectResponse(url="/login/github")


@router.get("/login/github")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/login/github/auth")
async def auth(request: Request, db: Session = Depends(get_session)):
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
    access_token = access_token_repo.get_by_kwargs(user_id=user.id)
    if not access_token:
        access_token = access_token_repo.create_from_kwargs(user_id=user.id)
    if github_user:
        request.session["user_id"] = str(user.id)
        request.session["access_token"] = str(access_token.token)
    return RedirectResponse(url="/")
