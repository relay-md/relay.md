# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from unittest.mock import patch
from uuid import UUID

import pytest

from backend import models, repos
from backend.models.billing import InvoiceStatus
from backend.utils.dates import last_day_of_month


@pytest.fixture
def get_webhook_payload():
    def func(reference_id: UUID):
        return {
            "id": "evt_1OPMoVB5jLfQ2TsFkv9zLcGZ",
            "object": "event",
            "api_version": "2023-10-16",
            "created": 1703067343,
            "data": {
                "object": {
                    "id": "cs_test_a1ardhex9OzbE4h9DcBZzXxwiZhRAhsukrxN6Os3PHOYcsKquX58VpzHgO",
                    "object": "checkout.session",
                    "after_expiration": None,
                    "allow_promotion_codes": None,
                    "amount_subtotal": 3000,
                    "amount_total": 3000,
                    "automatic_tax": {"enabled": False, "status": None},
                    "billing_address_collection": None,
                    "cancel_url": "http://localhost:5000/payment/failed",
                    "client_reference_id": str(reference_id),
                    "client_secret": None,
                    "consent": None,
                    "consent_collection": None,
                    "created": 1703067305,
                    "currency": "eur",
                    "currency_conversion": None,
                    "custom_fields": [],
                    "custom_text": {
                        "after_submit": None,
                        "shipping_address": None,
                        "submit": None,
                        "terms_of_service_acceptance": None,
                    },
                    "customer": "cus_PDoRlPaff7CDZO",
                    "customer_creation": "always",
                    "customer_details": {
                        "address": {
                            "city": None,
                            "country": "DE",
                            "line1": None,
                            "line2": None,
                            "postal_code": None,
                            "state": None,
                        },
                        "email": "fabian@chainsquad.com",
                        "name": "Fabian Schuh",
                        "phone": None,
                        "tax_exempt": "none",
                        "tax_ids": [],
                    },
                    "customer_email": "fabian@chainsquad.com",
                    "expires_at": 1703153705,
                    "invoice": "in_1OPMoSB5jLfQ2TsFGqEyEFbO",
                    "invoice_creation": None,
                    "livemode": False,
                    "locale": None,
                    "metadata": {},
                    "mode": "subscription",
                    "payment_intent": None,
                    "payment_link": None,
                    "payment_method_collection": "always",
                    "payment_method_configuration_details": None,
                    "payment_method_options": None,
                    "payment_method_types": ["card"],
                    "payment_status": "paid",
                    "phone_number_collection": {"enabled": False},
                    "recovered_from": None,
                    "setup_intent": None,
                    "shipping_address_collection": None,
                    "shipping_cost": None,
                    "shipping_details": None,
                    "shipping_options": [],
                    "status": "complete",
                    "submit_type": None,
                    "subscription": "sub_1OPMoSB5jLfQ2TsF5Yk9NCeY",
                    "success_url": "http://localhost:5000/payment/success",
                    "total_details": {
                        "amount_discount": 0,
                        "amount_shipping": 0,
                        "amount_tax": 0,
                    },
                    "ui_mode": "hosted",
                    "url": None,
                }
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {"id": None, "idempotency_key": None},
            "type": "checkout.session.completed",
        }

    return func


def test_create_invoice(
    dbsession, account, get_webhook_payload, web_client, create_team
):
    team = create_team("private_team")
    billing_repo = repos.InvoiceRepo(dbsession)
    products = [
        models.OrderItem(
            name="Foobar",
            quantity=10,
            price=3000,
            description="Foobar",
            team_id=team.id,
            stripe_key="team-yearly",
        )
    ]
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
    invoice = billing_repo.create(
        models.Invoice(
            user_id=account.id,
            customer=person,
            products=products,
        )
    )

    webhook_payload = get_webhook_payload(invoice.id)

    with patch("stripe.Webhook.construct_event", return_value=webhook_payload):
        req = web_client.post(
            "/payment/stripe/webhook",
            json=webhook_payload,
            auth=("foo", "bar"),
            headers={"stripe-signature": "foobar"},
        )

    req.raise_for_status()
    assert "error" not in req.json()

    dbsession.commit()
    dbsession.refresh(invoice)
    assert invoice.payment_status == InvoiceStatus.COMPLETED
    dbsession.refresh(team)

    assert team.paid_until == last_day_of_month(
        datetime.utcnow() + timedelta(days=30 * 10)
    )
