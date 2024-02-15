# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Query, Request
from starlette.responses import HTMLResponse

from ..database import Session, get_session
from ..exceptions import LoginRequiredException
from ..repos.document import DocumentRepo
from ..repos.user import User
from ..templates import templates
from ..utils.user import get_optional_user, require_user

router = APIRouter(prefix="")


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=["web"],
)
async def welcome(
    request: Request,
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("welcome.pug", context=dict(**locals()))


@router.get(
    "/profile",
    response_class=HTMLResponse,
    tags=["web"],
)
async def profile(
    request: Request,
    user: User = Depends(require_user),
):
    return templates.TemplateResponse("profile.pug", context=dict(**locals()))


@router.get(
    "/profile/documents",
    response_class=HTMLResponse,
    tags=["web"],
)
async def my_documents(
    request: Request,
    type: str = Query(default="owned"),
    size: int = Query(default=10),
    page: int = Query(default=0),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    repo = DocumentRepo(db)
    if type == "shared":
        documents = repo.get_shared_documents_for_user(user, page, size)
        total = repo.get_shared_documents_for_user_count(user)
    else:
        documents = repo.get_my_documents(user, page, size)
        total = repo.get_my_documents_count(user)
    return templates.TemplateResponse("documents.pug", context=dict(**locals()))


@router.get(
    "/blog",
    response_class=HTMLResponse,
    tags=["web"],
)
async def blog(
    request: Request,
    user: User = Depends(get_optional_user),
    db: Session = Depends(get_session),
):
    document_repo = DocumentRepo(db)
    articles = document_repo.latest_news()
    access_token = (
        request.session.get("access_token") or "empty"
    )  # in case no user exists
    return templates.TemplateResponse("blog.pug", context=dict(**locals()))


@router.get(
    "/documentation/plugins/obsidian",
    response_class=HTMLResponse,
    tags=["web"],
)
async def obsidian_plugin(
    request: Request,
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("plugin.pug", context=dict(**locals()))


@router.get(
    "/documentation/relay/basics",
    response_class=HTMLResponse,
    tags=["web"],
)
async def relay_basics(
    request: Request,
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("howto-relay.pug", context=dict(**locals()))


@router.get(
    "/tos",
    response_class=HTMLResponse,
    tags=["web"],
)
async def tos(
    request: Request,
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("tos.pug", context=dict(**locals()))


@router.get(
    "/pricing",
    response_class=HTMLResponse,
    tags=["web"],
)
async def pricing(
    request: Request,
    user: User = Depends(get_optional_user),
    team_name: str = Query(""),
):
    if team_name and not user:
        raise LoginRequiredException(next_url=request.url)
    return templates.TemplateResponse("pricing.pug", context=dict(**locals()))
