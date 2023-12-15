# -*- coding: utf-8 -*-
import abc
import logging
from datetime import datetime, timedelta
from uuid import UUID

from ..config import get_config
from ..database import Session
from ..exceptions import BadRequest, BillingException
from ..models.billing import (
    Invoice,
    InvoiceStatus,
    RecurringPaymentToken,
)
from ..utils.dates import last_day_of_month
from .base import DatabaseAbstractRepository
from .team import TeamRepo

log = logging.getLogger(__name__)


class AbstractPaymentGateway:
    @abc.abstractmethod
    def get_payment_link(self, invoice: Invoice):
        pass

    @abc.abstractmethod
    def get_payment_status(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_payment_session(self, **kwargs):
        pass

    @abc.abstractmethod
    def process_webhook(self, webhook):
        pass

    @abc.abstractmethod
    def subscription_payment(self, invoice: Invoice):
        pass


class AdyenPayments(AbstractPaymentGateway):
    def __init__(self, *args, **kwargs):
        import Adyen

        super().__init__(*args, **kwargs)

        self.adyen = Adyen.Adyen()
        self.adyen.payment.client.xapikey = get_config().ADYEN_API_KEY
        self.adyen.payment.client.platform = "test"  # change to live for production
        self.adyen.payment.client.merchant_account = get_config().ADYEN_MERCHANT_ACCOUNT

    def get_payment_link(self, invoice: Invoice):
        request = dict(
            amount=dict(
                value=invoice.total_amount,
                currency="EUR",
            ),
            merchantAccount=get_config().ADYEN_MERCHANT_ACCOUNT,
            returnUrl=get_config().ADYEN_RETURN_URL,
            reference=str(invoice.id),
            mode="hosted",
            themeId=get_config().ADYEN_THEME_ID,
            countryCode=invoice.customer.country_code,
            telephoneNumber=f"{invoice.customer.phone_country_code}{invoice.customer.phone_number}",
            # Recurring configurations for subscription:
            # recurringFrequency=invoice.payment.days_between_payments,
            # shopperInteraction="Ecommerce",
            shopperReference=str(invoice.user_id),
            storePaymentMethod=True,
            recurringProcessingModel="Subscription",
            mandate=dict(
                amount=invoice.total_amount,
                amountRule="exact",
                billingAttemptsRule="on",
                billingDay="1",
                endsAt="2030-12-31",  # FIXME:
                frequency="monthly",
            ),
        )
        result = self.adyen.checkout.payments_api.sessions(request)
        if result.status_code != 201:
            log.error(result.message)
            raise BillingException("Payment Provider refused session")
        message = result.message
        invoice.payment_provider_reference = message["id"]
        return result.message["url"]

    def get_payment_session(self, invoice: Invoice):
        request = dict(
            amount=dict(
                value=invoice.total_amount,
                currency="EUR",
            ),
            merchantAccount=get_config().ADYEN_MERCHANT_ACCOUNT,
            returnUrl=get_config().ADYEN_RETURN_URL,
            reference=str(invoice.id),
            countryCode=invoice.customer.country_code,
            lineItems=[
                dict(
                    id=str(p.id),
                    amountIncludingTax=p.price,
                    quantity=p.quantity,
                    brand=p.name,
                    description=p.description,
                )
                for p in invoice.products
            ],
            # Recurring configurations for subscription:
            recurringProcessingModel="Subscription",
            shopperInteraction="Ecommerce",
            shopperReference=str(invoice.user_id),
            storePaymentMethod=True,
        )
        result = self.adyen.checkout.payments_api.sessions(request)
        if result.status_code != 201:
            log.error(result.message)
            raise BadRequest(
                f"Payment Provider refused session for {result.message['refusalReason']}"
            )
        return result.message

    def get_payment_status(
        self,
        session_id: str,
        session_result: str,
    ):
        request = dict(sessionResult=session_result)
        result = self.adyen.checkout.payments_api.get_result_of_payment_session(
            session_id, query_parameters=request
        )
        return result.message["status"]

    def process_webhook(self, db: Session, webhook):
        for notification in webhook["notificationItems"]:
            item = notification["NotificationRequestItem"]
            event_code = item["eventCode"]
            additional_data = item["additionalData"]
            invoice_id = item["merchantReference"]
            invoice_repo = InvoiceRepo(db)
            invoice = invoice_repo.get_by_id(UUID(invoice_id))
            if not invoice:
                continue

            # payment was authorized
            if event_code == "AUTHORISATION":
                log.info(f"Payment was authorized for {invoice.id=}")
                if item["success"]:
                    invoice_repo.succeed_invoice_payment(invoice)
                else:
                    invoice_repo.update(invoice, payment_failure_reason=item["reason"])

            # in case we receive subscription data
            if event_code == "RECURRING_CONTRACT":
                log.info(f"Payment Subscription contract was created for {invoice.id=}")
                recurring_repo = RecurringPaymentTokenRepo(db)
                recurring_item = dict(
                    user_id=UUID(additional_data.get("recurring.shopperReference")),
                    recurringDetailReference=additional_data.get(
                        "recurring.recurringDetailReference"
                    ),
                    originalReference=item.get(
                        "originalReference", item.get("pspReference")
                    ),
                    pspReference=item.get("pspReference"),
                )
                # Uniq entries only
                if not recurring_repo.get_by_kwargs(**recurring_item):
                    recurring_repo.create_from_kwargs(**recurring_item)

    def subscription_payment(self, invoice: Invoice):
        # FIXME: is this always the best choice: "0"
        token = invoice.user.recurring_payment_tokens[0]
        request = dict(
            paymentMethod=dict(
                type="scheme", storedPaymentMethodId=token.recurringDetailReference
            ),
            shopperReference=str(invoice.user_id),
            shopperInteraction="ContAuth",
            recurringProcessingModel="Subscription",
            amount=dict(
                value=invoice.total_amount,
                currency="EUR",
            ),
            merchantAccount=get_config().ADYEN_MERCHANT_ACCOUNT,
            returnUrl=get_config().ADYEN_RETURN_URL,
            reference=str(invoice.id),
            # countryCode=invoice.customer.country_code,
        )
        result = self.adyen.checkout.payments_api.payments(request)
        if result.status_code != 200:
            raise BadRequest(
                f"Payment Provider refused session for {result.message['refusalReason']}"
            )
        message = result.message
        if message.get("resultCode") == "Authorised":
            # FIXME: do seomthing in the db to indicate subsequent payments are
            # fine now too
            pass
        return result.message


class InvoiceRepo(DatabaseAbstractRepository):
    ORM_Model = Invoice

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment = AdyenPayments()

    def get_payment_session(self, invoice: Invoice):
        return self.payment.get_payment_session(invoice)

    def get_payment_link(self, invoice: Invoice):
        return self.payment.get_payment_link(invoice)

    def get_payment_status(self, **kwargs):
        return self.payment.get_payment_status(**kwargs)

    def process_webhook(self, webhook):
        return self.payment.process_webhook(self._db, webhook)

    def subscription_payment(self, invoice: Invoice):
        return self.payment.subscription_payment(invoice)

    def succeed_invoice_payment(self, invoice: Invoice):
        # update each product if neede
        team_repo = TeamRepo(self._db)
        for product in invoice.products:
            if product.team_id:
                months = product.quantity
                # always fill next month
                now = datetime.utcnow()
                paid_until = last_day_of_month(now + timedelta(days=months * 30))
                team_repo.update(product.team, paid_until=paid_until)
        return self.update(
            invoice, payment_status=InvoiceStatus.COMPLETED, paid_at=datetime.utcnow()
        )


class RecurringPaymentTokenRepo(DatabaseAbstractRepository):
    ORM_Model = RecurringPaymentToken
