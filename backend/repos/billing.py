# -*- coding: utf-8 -*-
import logging

from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.common.common import (
    Address,
    CustomerRequest,
    Phone,
    Product,
)
from checkout_sdk.common.enums import PaymentSourceType
from checkout_sdk.environment import Environment
from checkout_sdk.exception import (
    CheckoutApiException,
    CheckoutArgumentException,
    CheckoutAuthorizationException,
)
from checkout_sdk.payments.hosted.hosted_payments import (
    HostedPaymentsSessionRequest,
)
from checkout_sdk.payments.payments_previous import BillingInformation
from checkout_sdk.sessions.sessions import Recurring

from ..config import get_config
from ..exceptions import BillingException
from ..models.billing import Invoice
from .base import DatabaseAbstractRepository

log = logging.getLogger(__name__)


class InvoiceRepo(DatabaseAbstractRepository):
    ORM_Model = Invoice

    def get_checkoutcom_payment_link(
        self,
        invoice: Invoice,
    ):
        self.api = (
            CheckoutSdk.builder()
            .secret_key(get_config().CHECKOUTCOM_CLIENT_SECRET)
            .public_key(get_config().CHECKOUTCOM_CLIENT_ID)
            .environment(Environment.sandbox())
            .build()
        )
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

        request.amount = sum([x.quantity * x.price for x in request_products])

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

    def get_payment_link(self, invoice: Invoice):
        return self.get_checkoutcom_payment_link(invoice)
