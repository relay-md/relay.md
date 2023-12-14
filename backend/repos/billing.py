# -*- coding: utf-8 -*-
import abc
import logging
from uuid import UUID

from ..config import get_config
from ..database import Session
from ..exceptions import BadRequest, BillingException
from ..models.billing import (
    Invoice,
    InvoiceStatus,
    RecurringPaymentToken,
)
from .base import DatabaseAbstractRepository

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


class CheckoutComPayments(AbstractPaymentGateway):
    def __init__(self, *args, **kwargs):
        from checkout_sdk.checkout_sdk import CheckoutSdk
        from checkout_sdk.environment import Environment

        super().__init__(*args, **kwargs)
        self.api = (
            CheckoutSdk.builder()
            .secret_key(get_config().CHECKOUTCOM_CLIENT_SECRET)
            .public_key(get_config().CHECKOUTCOM_CLIENT_ID)
            .environment(Environment.sandbox())
            .build()
        )

    def get_payment_link(self, invoice: Invoice):
        from checkout_sdk.common.common import (
            Address,
            CustomerRequest,
            Phone,
            Product,
        )
        from checkout_sdk.common.enums import PaymentSourceType
        from checkout_sdk.exception import (
            CheckoutApiException,
            CheckoutArgumentException,
            CheckoutAuthorizationException,
        )
        from checkout_sdk.payments.hosted.hosted_payments import (
            HostedPaymentsSessionRequest,
        )
        from checkout_sdk.payments.payments_previous import (
            BillingInformation,
        )
        from checkout_sdk.sessions.sessions import Recurring

        phone = Phone()
        phone.country_code = invoice.customer.phone_country_code
        phone.number = invoice.customer.phone_number

        address = Address()
        address.address_line1 = invoice.customer.address_line1
        address.address_line2 = invoice.customer.address_line2
        address.city = invoice.customer.city
        address.state = invoice.customer.state
        address.zip = invoice.customer.zip
        address.country = invoice.customer.country_code

        customer_request = CustomerRequest()
        customer_request.email = invoice.customer.email
        customer_request.name = invoice.customer.name

        billing_information = BillingInformation()
        billing_information.address = address
        billing_information.phone = phone

        request_products = list()
        for product in invoice.products:
            prod = Product()
            prod.name = product.name
            prod.quantity = product.quantity
            prod.price = product.price
            request_products.append(prod)

        request = HostedPaymentsSessionRequest()
        request.currency = "EUR"  # Currency.EUR
        request.billing = billing_information
        request.success_url = "https://docs.checkout.com/payments/success"
        request.failure_url = "https://docs.checkout.com/payments/failure"
        request.cancel_url = "https://docs.checkout.com/payments/cancel"
        request.payment_type = "Recurring"

        request.payment_plan = Recurring()
        request.payment_plan.days_between_payments = (
            invoice.payment.days_between_payments
        )
        request.payment_plan.expiry = invoice.payment.expiry.strftime("%Y%m%d")
        request.processing_channel_id = get_config().CHECKOUTCOM_CHANNEL_ID

        request.amount = invoice.total_amount

        request.reference = str(invoice.id)

        request.description = get_config().CHECKOUTCOM_DESCRIPTION

        request.customer = customer_request
        request.products = request_products

        # https://www.checkout.com/docs/payments/accept-payments/create-a-payment-link/manage-payment-links#Payment_methods
        request.allow_payment_methods = [
            PaymentSourceType.CARD,
            PaymentSourceType.GIROPAY,
            PaymentSourceType.IDEAL,
            PaymentSourceType.PAYPAL,
            PaymentSourceType.SOFORT,
            # PaymentSourceType.SEPA,
            # PaymentSourceType.KLARNA,
        ]

        try:
            response = self.api.hosted_payments.create_hosted_payments_page_session(
                request
            )
        except CheckoutApiException as err:
            # API error
            log.error(err.http_metadata)
            log.error(err.error_details)
            log.error(err.error_type)
            raise BillingException("Could not process payment")
        except CheckoutArgumentException as err:
            log.error(err)
            raise BillingException("Could not process payment")

        except CheckoutAuthorizationException as err:
            log.error(err)
            raise BillingException("Could not process payment")

        return response._links.redirect.href

    def get_payment_status(self, **kwargs):
        return "completed"

    def get_payment_session(self, **kwargs):
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
                    invoice_repo.update(invoice, payment_status=InvoiceStatus.COMPLETED)
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
                    invoice_id=invoice.id,
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

        if get_config().PAYMENT_PROVIDER == "checkoutcom":
            self.payment = CheckoutComPayments()
        else:
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


class RecurringPaymentTokenRepo(DatabaseAbstractRepository):
    ORM_Model = RecurringPaymentToken
