import json
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from starlette.responses import HTMLResponse, RedirectResponse
from ..database import get_session, Session
from .. import oauth, models
from ..models.landingpage import LandingPageEmail

router = APIRouter(prefix="/v0")


class EmailSubmitRequest(BaseModel):
    email: EmailStr


@router.post("/mail/submit")
async def submitmail(payload: EmailSubmitRequest, db: Session = Depends(get_session)) -> str:
    new = LandingPageEmail(email=payload.email)
    db.add(new)
    db.commit()
    return """
        <div class="notification is-success">
        Thank you for submitting your address. Please check your mailbox to
        opt-in.
        </div>
    """
