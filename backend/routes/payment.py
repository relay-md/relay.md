# -*- coding: utf-8 -*-

import secrets
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import HTMLResponse

from ..config import Settings, get_config
from ..database import Session, get_session
from ..exceptions import BadRequest
from ..models.billing import InvoiceStatus
from ..repos.billing import InvoiceRepo, RecurringPaymentTokenRepo
from ..repos.user import User
from ..templates import templates
from ..utils.user import get_optional_user

router = APIRouter(prefix="/payment")
security = HTTPBasic()


def required_webhook_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    forbidden = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect credentials",
        headers={"WWW-Authenticate": "Basic"},
    )
    allowed = get_config().PAYMENT_BASIC_AUTH_WHITELIST
    allowed_set = list(filter(lambda x: x[0] == credentials.username, allowed))
    if not allowed_set:
        raise forbidden
    allowed_set = allowed_set[0]
    credentials.password.encode("utf8")
    if not secrets.compare_digest(
        credentials.password.encode("utf8"), allowed_set[1].encode("utf8")
    ):
        raise forbidden
    return credentials.username


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
):
    invoice_repo = InvoiceRepo(db)
    invoice = invoice_repo.get_by_id(invoice_id)
    client_key = config.ADYEN_CLIENT_KEY
    if not invoice:
        raise BadRequest("Invalid invoice ID")
    return templates.TemplateResponse("adyen-component.pug", context=dict(**locals()))


@router.post(
    "/adyen/session/{invoice_id}",
    tags=["web"],
)
async def adyen_session_for_invoice(
    invoice_id: UUID,
    request: Request,
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
):
    invoice_repo = InvoiceRepo(db)
    invoice = invoice_repo.get_by_id(invoice_id)
    if not invoice:
        raise BadRequest("Invalid invoice ID")
    return invoice_repo.get_payment_session(invoice)


@router.get(
    "/success",
    response_class=HTMLResponse,
    tags=["web"],
)
async def payment_success(
    request: Request,
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("payment-success.pug", context=dict(**locals()))


@router.get(
    "/adyen/success",
    response_class=HTMLResponse,
    tags=["web"],
)
async def adyen_success(
    request: Request,
    config: Settings = Depends(get_config),
    sessionId: str = Query(default=""),
    sessionResult: str = Query(default=""),
    db: Session = Depends(get_session),
    user: User = Depends(get_optional_user),
):
    if not sessionId or not sessionResult:
        raise BadRequest("Missing sessionId or sessionResult")
    invoice_repo = InvoiceRepo(db)
    status = invoice_repo.get_payment_status(
        session_id=sessionId, session_result=sessionResult
    )
    if status != "completed":
        raise BadRequest(f"Payment went wrong? Status is {status}")
    return RedirectResponse(url=request.url_for("payment_success"))


@router.post(
    "/adyen/webhook",
    tags=["web"],
)
async def adyen_webhook(
    request: Request,
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
    username: str = Depends(required_webhook_basic_auth),
):
    from rich import print

    webhook = await request.json()
    print(webhook)
    invoice_repo = InvoiceRepo(db)
    try:
        for notification in webhook["notificationItems"]:
            item = notification["NotificationRequestItem"]
            additional_data = item["additionalData"]
            invoice_id = item["merchantReference"]
            invoice = invoice_repo.get_by_id(UUID(invoice_id))
            if not invoice:
                continue
            if item["success"]:
                invoice_repo.update(invoice, payment_status=InvoiceStatus.COMPLETED)
            else:
                invoice_repo.update(invoice, payment_failure_reason=item["reason"])

            # in case we receive subscription data
            if additional_data.get("recurring.shopperReference"):
                recurring_repo = RecurringPaymentTokenRepo(db)
                recurring_repo.create_from_kwargs(
                    user_id=UUID(additional_data.get("recurring.shopperReference")),
                    recurringDetailReference=additional_data.get(
                        "recurring.recurringDetailReference"
                    ),
                    originalReference=item.get("originalReference"),
                    pspReference=item.get("pspReference"),
                    invoice_id=invoice.id,
                )
    except Exception as e:
        return dict(error=dict(message=str(e)))

    return dict(success=True, message="[accepted]")
