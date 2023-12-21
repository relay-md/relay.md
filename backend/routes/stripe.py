# -*- coding: utf-8 -*-

from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from starlette.responses import HTMLResponse

from ..config import Settings, get_config
from ..database import Session, get_session
from ..exceptions import BadRequest
from ..repos.billing import InvoiceRepo
from ..repos.user import User
from ..templates import templates
from ..utils.http import required_basic_auth
from ..utils.user import get_optional_user

router = APIRouter(prefix="/payment")


@router.get(
    "/success",
    response_class=HTMLResponse,
    tags=["web"],
)
async def payment_success(
    request: Request,
    config: Settings = Depends(get_config),
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("payment-success.pug", context=dict(**locals()))


@router.get(
    "/failed",
    response_class=HTMLResponse,
    tags=["web"],
)
async def payment_failed(
    request: Request,
    config: Settings = Depends(get_config),
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("payment-failed.pug", context=dict(**locals()))


@router.get(
    "/error",
    response_class=HTMLResponse,
    tags=["web"],
)
async def payment_error(
    request: Request,
    config: Settings = Depends(get_config),
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("payment-error.pug", context=dict(**locals()))


@router.get(
    "/invoice/{invoice_id}",
    response_class=HTMLResponse,
    tags=["web"],
)
async def payment_invoice(
    invoice_id: UUID,
    request: Request,
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
    user: User = Depends(get_optional_user),
):
    invoice_repo = InvoiceRepo(db)
    invoice = invoice_repo.get_by_id(invoice_id)
    if not invoice:
        raise BadRequest("Invalid invoice ID")
    if invoice.paid_at is None:
        return RedirectResponse(
            url=request.url_for("stripe_session_for_invoice", invoice_id=invoice_id)
        )
    return "paid"


@router.get(
    "/stripe/session/{invoice_id}",
    tags=["web"],
)
async def stripe_session_for_invoice(
    invoice_id: UUID,
    request: Request,
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
):
    invoice_repo = InvoiceRepo(db)
    invoice = invoice_repo.get_by_id(invoice_id)
    try:
        checkout_session = invoice_repo.get_payment_session(invoice)
        return RedirectResponse(url=checkout_session.url, status_code=303)
    except Exception as e:
        raise BadRequest(e)


@router.post(
    "/stripe/webhook",
    tags=["web"],
)
async def stripe_webhook(
    request: Request,
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
    username: str = Depends(required_basic_auth),
):
    invoice_repo = InvoiceRepo(db)
    try:
        await invoice_repo.process_webhook(request)
    except Exception as e:
        return dict(error=dict(message=str(e)))
    return dict(success=True, message="accepted")
