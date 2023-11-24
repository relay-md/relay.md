# -*- coding: utf-8 -*-

from uuid import UUID

from fastapi import APIRouter, Depends, Form, Request, status
from starlette.responses import HTMLResponse, RedirectResponse

from ..repos.user import User
from ..templates import templates
from ..utils.user import get_optional_user

router = APIRouter(prefix="")


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=["web"],
)
async def welcome(request: Request, user: User = Depends(get_optional_user)):
    return templates.TemplateResponse("welcome.html", context=dict(**locals()))


@router.post("/document")
async def get_document(request: Request, id: str = Form(default="")):
    fail = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    if not id:
        return fail
    try:
        UUID(id)
    except Exception:
        return fail
    return RedirectResponse(
        url=request.url_for("get_document_from_id", id=id),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/document/{id}")
async def get_document_from_id(request: Request, id: str):
    id_uuid = UUID(id)
    access_token = request.session["access_token"]
    return templates.TemplateResponse("viewer.html", context=dict(**locals()))
