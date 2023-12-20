# -*- coding: utf-8 -*-
import abc
import logging
from datetime import datetime, timedelta

import stripe

from ..config import get_config
from ..exceptions import BadRequest
from ..models.billing import Invoice, InvoiceStatus
from ..utils.dates import last_day_of_month
from .base import DatabaseAbstractRepository
from .team import TeamRepo

log = logging.getLogger(__name__)


class AbstractPaymentGateway:
    @abc.abstractmethod
    def get_payment_session(self, **kwargs):
        pass

    @abc.abstractmethod
    async def process_webhook(self, request):
        pass


class StripePayments(AbstractPaymentGateway):
    def __init__(self):
        stripe.api_key = get_config().STRIPE_API_PRIVATE_KEY

    def get_payment_session(self, invoice: Invoice):
        line_items = list()
        for item in invoice.products:
            prices = stripe.Price.list(
                lookup_keys=[item.stripe_key], expand=["data.product"]
            )
            line_items.append(
                {
                    "price": prices.data[0].id,
                    # we use quantity here because stipe uses a yearly
                    # subscription instead of 12 months
                    "quantity": 1,
                },
            )

        checkout_session = stripe.checkout.Session.create(
            client_reference_id=str(invoice.id),
            # FIXME: might want to create a stripe customer and reference to it
            # https://stripe.com/docs/api/checkout/sessions/create
            currency="EUR",
            customer_email=invoice.user.email,
            line_items=line_items,
            mode="subscription",
            success_url=f"{get_config().STRIPE_RETURN_URL_SUCCESS}",  # ?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=get_config().STRIPE_RETURN_URL_CANCEL,
        )
        return checkout_session

    async def process_webhook(self, db, request):
        sig_header = request.headers["stripe-signature"]
        try:
            event = stripe.Webhook.construct_event(
                await request.body(), sig_header, get_config().STRIPE_WEBHOOK_SECRET
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
            invoice_repo = InvoiceRepo(db)
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


class InvoiceRepo(DatabaseAbstractRepository):
    ORM_Model = Invoice

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment = StripePayments()

    def get_payment_session(self, invoice: Invoice):
        return self.payment.get_payment_session(invoice)

    async def process_webhook(self, request):
        return await self.payment.process_webhook(self._db, request)

    def succeed_invoice_payment(self, invoice: Invoice):
        log.info(f"Invoice {invoice.id} was just paid successfully")
        # update each product if neede
        team_repo = TeamRepo(self._db)
        for product in invoice.products:
            log.info(f" Invoice item {product.id} was just paid successfully")
            if product.team_id:
                log.info(f" Team {product.team.name} was just paid successfully")
                months = product.quantity
                # always fill next month
                now = datetime.utcnow()
                paid_until = last_day_of_month(now + timedelta(days=months * 30))
                team_repo.update(product.team, paid_until=paid_until)
        return self.update(
            invoice, payment_status=InvoiceStatus.COMPLETED, paid_at=datetime.utcnow()
        )
