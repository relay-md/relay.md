# -*- coding: utf-8 -*-
import logging
from typing import List

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
from ..schema import (
    BillingPersonalInformation,
    BillingProductInformation,
    BillingRecurringPaymentPlan,
)

log = logging.getLogger(__name__)


class BillingRepo:
    def get_payment_link(self):
        pass


class CheckoutComBillingRepo(BillingRepo):
    def __init__(self):
        self.api = (
            CheckoutSdk.builder()
            .secret_key(get_config().CHECKOUTCOM_CLIENT_SECRET)
            .public_key(get_config().CHECKOUTCOM_CLIENT_ID)
            .environment(Environment.sandbox())
            .build()
        )

    def get_payment_link(
        self,
        personal_information: BillingPersonalInformation,
        products: List[BillingProductInformation],
        payment_plan: BillingRecurringPaymentPlan,
    ):
        phone = Phone()
        phone.country_code = personal_information.phone_country_code
        phone.number = personal_information.phone_number

        address = Address()
        address.address_line1 = personal_information.address_line1
        address.address_line2 = personal_information.address_line2
        address.city = personal_information.city
        address.state = personal_information.state
        address.zip = personal_information.zip
        address.country = personal_information.country

        customer_request = CustomerRequest()
        customer_request.email = personal_information.email
        customer_request.name = personal_information.name

        billing_information = BillingInformation()
        billing_information.address = address
        billing_information.phone = phone

        request_products = list()
        for product in products:
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
        request.payment_plan.days_between_payments = payment_plan.days_between_payments
        request.payment_plan.expiry = payment_plan.expiry
        request.processing_channel_id = "pc_ildl7xfiu4yubf2xhvgst4h2wq"

        request.amount = sum([x.quantity * x.price for x in request_products])

        from uuid import uuid4

        request.reference = str(uuid4())

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
