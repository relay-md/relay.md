# -*- coding: utf-8 -*-

import requests
from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr

from ..config import config
from ..database import Session, get_session

router = APIRouter(prefix="/v0")


@router.post("/mail/submit")
async def submitmail(
    email: EmailStr = Form(),
    first_name: str = Form(),
    last_name: str = Form(),
    db: Session = Depends(get_session),
) -> str:
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
    req.raise_for_status()

    return """
        <div class="notification is-success">
        Thank you for submitting your address. Please check your mailbox to
        opt-in.
        </div>
    """
