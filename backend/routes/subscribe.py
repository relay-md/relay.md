# -*- coding: utf-8 -*-

from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse

from backend.repos.newsletter import NewsletterRepo

from ..database import Session, get_session
from ..exceptions import AlreadySubscribed

router = APIRouter(prefix="/mail")


@router.post("/validate", tags=["v0"])
async def validatemail(email: str = Form(default="")) -> HTMLResponse:
    error_msg = ""
    try:
        email = validate_email(email, check_deliverability=False)
        _ = email.normalized
    except EmailNotValidError:
        error_msg = '<p class="help is-danger">This email is invalid</p>'
    return HTMLResponse(error_msg)


@router.post("/submit", tags=["v0"])
async def submitmail(
    email: str = Form(default=None),
    db: Session = Depends(get_session),
) -> str:
    try:
        email = validate_email(email, check_deliverability=False)
        email = email.normalized
    except EmailNotValidError:
        return "invalid email"

    newsletter_repo = NewsletterRepo()
    try:
        newsletter_repo.subscribe(email)
    except AlreadySubscribed:
        return HTMLResponse(
            """
          <div class="notification is-warning">
          This email address has already registered
          </div>
          """
        )
    except Exception as exc:
        return str(exc)

    return HTMLResponse(
        """
        <div class="notification is-success">
        Thank you for submitting your address. Please check your mailbox to
        opt-in.
        </div>
    """
    )
