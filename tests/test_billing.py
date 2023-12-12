# -*- coding: utf-8 -*-
from datetime import date
from uuid import UUID

import pytest

from backend import models, repos
from backend.models.billing import InvoiceStatus


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


def test_create_invoice(dbsession, get_webhook_payload, web_client):
    billing_repo = repos.InvoiceRepo(dbsession)
    products = [models.ProductInformation(name="Foobar", quantity=10, price=3000)]
    person = models.PersonalInformation(
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
