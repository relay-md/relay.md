# -*- coding: utf-8 -*-
from datetime import date
from uuid import UUID

import pytest

from backend import models, repos
from backend.models.billing import InvoiceStatus


@pytest.fixture
def get_webhook_payload_recurring_contract():
    def func(reference_id: UUID, shopper_id: UUID):
        return {
            "live": "false",
            "notificationItems": [
                {
                    "NotificationRequestItem": {
                        "additionalData": {
                            "recurring.shopperReference": str(shopper_id),
                            "recurring.recurringDetailReference": "M5N7TQ4TG5PFWR50",
                            "hmacSignature": "YOUR_HMAC_SIGNATURE",
                            "shopperReference": "YOUR_SHOPPER_REFERENCE",
                            "checkoutSessionId": "******************",
                        },
                        "amount": {"currency": "US", "value": 0},
                        "eventCode": "RECURRING_CONTRACT",
                        "eventDate": "2023-06-20T16:09:48+02:00",
                        "merchantAccountCode": "YOUR_MERCHANT_ACCOUNT",
                        "merchantReference": str(reference_id),
                        "originalReference": "DZ4DPSHB4WD2WN82",
                        "paymentMethod": "mc",
                        "pspReference": "M5N7TQ4TG5PFWR50",
                        "reason": "",
                        "success": "true",
                    }
                }
            ],
        }

    return func


@pytest.fixture
def get_webhook_payload():
    def func(reference_id: UUID):
        return {
            "live": "false",
            "notificationItems": [
                {
                    "NotificationRequestItem": {
                        "additionalData": {
                            "authCode": "1234",
                            "totalFraudScore": "10",
                            "NAME2": "VALUE2",
                            "NAME1": "VALUE1",
                            "fraudCheck-6-ShopperIpUsage": "10",
                        },
                        "amount": {"currency": "EUR", "value": 10100},
                        "eventCode": "AUTHORISATION",
                        "eventDate": "2023-12-13T12:24:53+01:00",
                        "merchantAccountCode": "ChainSquadGmbH",
                        "merchantReference": str(reference_id),
                        "pspReference": "ZCLWCV5MP8JSTC82",
                        "reason": "1234:7777:12/2012",
                        "success": "true",
                    }
                }
            ],
        }

    return func


def test_create_invoice(dbsession, account, get_webhook_payload, web_client):
    billing_repo = repos.InvoiceRepo(dbsession)
    products = [models.ProductInformation(name="Foobar", quantity=10, price=3000)]
    person = models.PersonalInformation(
        user_id=account.id,
        name="Fabian Schuh",
        email="fabian@chainsquad.com",
        address_line1="Address 13, 24 Foobar",
        city="Erlangen",
        state="Bavaria",
        zip="91058",
        country_code="DE",
        phone_country_code="+49",
        phone_number="1706397354",
    )
    payment_plan = models.PaymentPlan(
        days_between_payments=30, expiry=date(2025, 12, 31)
    )
    invoice = billing_repo.create(
        models.Invoice(
            customer=person,
            products=products,
            payment=payment_plan,
        )
    )

    webhook_payload = get_webhook_payload(invoice.id)

    web_client.post("/payment/adyen/webhook", json=webhook_payload, auth=("foo", "bar"))

    dbsession.commit()
    dbsession.refresh(invoice)
    assert invoice.payment_status == InvoiceStatus.COMPLETED


def test_create_invoice_recurring(
    dbsession, account, get_webhook_payload_recurring_contract, web_client
):
    billing_repo = repos.InvoiceRepo(dbsession)
    products = [models.ProductInformation(name="Foobar", quantity=10, price=3000)]
    person = models.PersonalInformation(
        user_id=account.id,
        name="Fabian Schuh",
        email="fabian@chainsquad.com",
        address_line1="Address 13, 24 Foobar",
        city="Erlangen",
        state="Bavaria",
        zip="91058",
        country_code="DE",
        phone_country_code="+49",
        phone_number="1706397354",
    )
    payment_plan = models.PaymentPlan(
        days_between_payments=30, expiry=date(2025, 12, 31)
    )
    invoice = billing_repo.create(
        models.Invoice(
            customer=person,
            products=products,
            payment=payment_plan,
        )
    )

    webhook_payload = get_webhook_payload_recurring_contract(invoice.id, account.id)

    web_client.post("/payment/adyen/webhook", json=webhook_payload, auth=("foo", "bar"))

    dbsession.commit()
    dbsession.refresh(invoice)
    assert invoice.payment_status == InvoiceStatus.COMPLETED

    recurring_repo = repos.billing.RecurringPaymentTokenRepo(dbsession)
    token = recurring_repo.get_by_kwargs(invoice_id=invoice.id)
    assert token
    assert token.user_id == account.id
    assert token.recurringDetailReference == "M5N7TQ4TG5PFWR50"
    assert token.originalReference == "DZ4DPSHB4WD2WN82"
    assert token.pspReference == "M5N7TQ4TG5PFWR50"
    assert token.invoice_id == invoice.id
