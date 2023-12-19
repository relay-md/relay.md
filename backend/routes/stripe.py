# -*- coding: utf-8 -*-

import secrets
from uuid import UUID

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import HTMLResponse

from ..config import Settings, get_config
from ..database import Session, get_session
from ..exceptions import BadRequest
from ..repos.billing import InvoiceRepo
from ..repos.user import User
from ..templates import templates
from ..utils.user import get_optional_user

router = APIRouter(prefix="/payment")
security = HTTPBasic()
stripe.api_key = get_config().STRIPE_API_PRIVATE_KEY

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = "whsec_G7uhdFNrr0HlRXktjVJpXB71hDLtxdyl"


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
    return templates.TemplateResponse("stripe-component.pug", context=dict(**locals()))


@router.post(
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
        prices = stripe.Price.list(
            lookup_keys=["team-monthly"], expand=["data.product"]  # FIXME:
        )
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=str(invoice.id),
            # FIXME: might want to create a stripe customer and reference to it
            # https://stripe.com/docs/api/checkout/sessions/create
            currency="EUR",
            customer_email=invoice.user.email,
            line_items=[
                {
                    "price": prices.data[0].id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=f"{get_config().STRIPE_RETURN_URL_SUCCESS}",  # ?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=get_config().STRIPE_RETURN_URL_CANCEL,
        )
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
    username: str = Depends(required_webhook_basic_auth),
):
    from rich import print

    await request.json()
    invoice_repo = InvoiceRepo(db)
    """
    invoice_repo.process_webhook(webhook)
    try:
        invoice_repo.process_webhook(webhook)
    except Exception as e:
        return dict(error=dict(message=str(e)))
    return dict(success=True, message="[accepted]")
    """
    sig_header = request.headers["stripe-signature"]
    try:
        event = stripe.Webhook.construct_event(
            await request.body(), sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]
    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]
    elif event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        invoice_id = session["client_reference_id"]
        invoice = invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise BadRequest("Invalid invoice ID")
        invoice_repo.succeed_invoice_payment(invoice)
    elif event["type"] == "checkout.session.expired":
        session = event["data"]["object"]
    else:
        print("Unhandled event type {}".format(event["type"]))
    print(event)

    return dict(success=True)
