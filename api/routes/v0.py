# -*- coding: utf-8 -*-

import requests
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from ..config import config
from ..database import Session, get_session

router = APIRouter(prefix="/v0")


class EmailSubmitRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


@router.post("/mail/submit")
async def submitmail(
    payload: EmailSubmitRequest, db: Session = Depends(get_session)
) -> str:
    req = requests.post(
        f"https://{config.MAILCHIMP_API_SERVER}.api.mailchimp.com/3.0/lists/{config.MAILCHIMP_LIST_ID}/members",
        auth=("key", config.MAILCHIMP_API_KEY),
        headers={"content-type": "application/json"},
        json={
            "email_address": payload.email,
            "status": "pending",
            "merge_fields": {"FNAME": payload.first_name, "LNAME": payload.last_name},
        },
    )
    req.raise_for_status()

    return """
        <div class="notification is-success">
        Thank you for submitting your address. Please check your mailbox to
        opt-in.
        </div>
    """
