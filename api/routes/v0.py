# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

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
