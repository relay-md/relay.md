# -*- coding: utf-8 -*-

from uuid import UUID

from fastapi import APIRouter, Depends, Form, Request, status
from starlette.responses import RedirectResponse

from ..repos.user import User
from ..templates import templates
from ..utils.user import get_optional_user

router = APIRouter(prefix="")


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
async def get_document_from_id(
    request: Request,
    id: str,
    user: User = Depends(get_optional_user),
):
    access_token = (
        request.session.get("access_token") or "empty"
    )  # in case no user exists
    return templates.TemplateResponse("viewer.pug", context=dict(**locals()))
