# -*- coding: utf-8 -*-

import requests
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Depends, Form
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from pydantic import EmailStr, ValidationError

from ..config import config
from ..database import Session, get_session

router = APIRouter(prefix="/mail")


@router.post("/validate", tags=["v0"])
async def validatemail(email: str = Form(default="")) -> str:
    danger = ""
    error = ""
    error_msg = ""
    try:
        email = validate_email(email, check_deliverability=False)
        email = email.normalized
    except EmailNotValidError:
        danger = "is-danger"
        error = """<span class="icon is-small is-right">
                    <i class="fas fa-exclamation-triangle"></i>
                   </span>"""
        error_msg = '<p class="help is-danger">This email is invalid</p>'
    return HTMLResponse(
        f"""
                <div class="field" hx-target="this" hx-swap="outerHTML">
                  <div class="control has-icons-left has-icons-right">
                    <input class="input is-medium {danger}"
                           type="email"
                           name="email"
                           value="{email}"
                           placeholder=""
                           hx-post="https://api.relay.md/v0/mail/validate" />
                    <span class="icon is-small is-left">
                      <i class="fas fa-envelope"></i>
                    </span>
                    {error}
                  </div>
                 {error_msg}
                </div>
    """
    )


@router.post("/submit", tags=["v0"])
async def submitmail(
    email: str = Form(default=None),
    first_name: str = Form(default=None),
    last_name: str = Form(default=None),
    db: Session = Depends(get_session),
) -> str:
    if not email or not first_name or not last_name:
        raise HTTPException(
            status_code=400, detail="email, first_name and last_name are required"
        )

    try:
        email = EmailStr(email)
    except ValidationError:
        return "invalid email"

    req = requests.post(
        f"https://{config.MAILCHIMP_API_SERVER}.api.mailchimp.com/3.0/lists/{config.MAILCHIMP_LIST_ID}/members",
        auth=("key", config.MAILCHIMP_API_KEY),
        headers={"content-type": "application/json"},
        json={
            "email_address": email,
            "status": "pending",
            "merge_fields": {"FNAME": first_name, "LNAME": last_name},
        },
    )
    res = req.json()
    print(res)
    if not req.ok:
        if res.get("title") == "Member Exists":
            return HTMLResponse(
                """
            <div class="notification is-warning">
            This email address has already registered
            </div>
            """
            )
        else:
            return res.get("title", "An error occured!")

    return HTMLResponse(
        """
        <div class="notification is-success">
        Thank you for submitting your address. Please check your mailbox to
        opt-in.
        </div>
    """
    )
