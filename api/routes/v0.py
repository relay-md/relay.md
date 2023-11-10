# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exception import HTTPException
from pydantic import BaseModel, EmailStr
from starlette.responses import RedirectResponse

from ..database import Session, get_session
from ..models.landingpage import LandingPageEmail

router = APIRouter(prefix="/v0")


class EmailSubmitRequest(BaseModel):
    email: EmailStr


@router.post("/mail/submit")
async def submitmail(
    payload: EmailSubmitRequest, db: Session = Depends(get_session)
) -> str:
    new = LandingPageEmail(email=payload.email)
    db.add(new)
    db.commit()
    return """
        <div class="notification is-success">
        Thank you for submitting your address. Please check your mailbox to
        opt-in.
        </div>
    """


@router.post("/mail/confirm/{id}/{confirm_code}")
async def confirm_mail(
    id: UUID, confirm_code: UUID, db: Session = Depends(get_session)
) -> str:
    mail = db.get(LandingPageEmail, id)
    if not mail:
        raise HTTPException(status_code=404, detail="user not found")
    mail.confirm(confirm_code)
    db.commit()
    return RedirectResponse(url="https://channel.md/email/confirmed.html")
