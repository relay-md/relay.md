# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import PlainTextResponse
from starlette.responses import HTMLResponse

from ..config import Settings, get_config
from ..repos.user import User
from ..templates import templates
from ..utils.email import send_email
from ..utils.user import get_optional_user, require_user

router = APIRouter(prefix="/contact")


@router.get(
    "",
    response_class=HTMLResponse,
    tags=["web"],
)
async def contact(
    request: Request,
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("contact.pug", context=dict(**locals()))


@router.post(
    "",
    response_class=PlainTextResponse,
    tags=["web"],
)
async def contact_post(
    request: Request,
    user: User = Depends(require_user),
    config: Settings = Depends(get_config),
    name: str = Form(default=""),
    email: str = Form(default=""),
    message: str = Form(default=""),
):
    send_email(
        config.MAIL_ADMIN,
        f"[relay.md - contact form] {name}",
        "mail/contact.html",
        sender=email,
        **locals(),
    )
    return """
    <div class="notification is-success">Email has been sent</div>
    """
