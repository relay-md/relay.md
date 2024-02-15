# -*- coding: utf-8 -*-
from unittest.mock import patch
from uuid import UUID

import pytest

from backend import models, repos
from backend.models.billing import InvoiceStatus


@pytest.fixture
def get_webhook_payload():
    def func(reference_id: UUID):
        return {
            "id": "evt_1OPMoVB5jLfQ2TsFkv9zLcGZ",
            "object": "event",
            "data": {
                "object": {
                    "id": "cs_test_a1ardhex9OzbE4h9DcBZzXxwiZhRAhsukrxN6Os3PHOYcsKquX58VpzHgO",
                    "object": "checkout.session",
                    "client_reference_id": str(reference_id),
                    "customer": "cus_PDoRlPaff7CDZO",
                    "invoice": "in_1OPMoSB5jLfQ2TsFGqEyEFbO",
                    "mode": "subscription",
                    "payment_status": "paid",
                    "status": "complete",
                    "subscription": "sub_1OPMoSB5jLfQ2TsF5Yk9NCeY",
                }
            },
            "type": "checkout.session.completed",
        }

    return func


@pytest.fixture
def get_get_full_session():
    def func(invoice_id: UUID, subscription_id: UUID):
        return {
            "id": "cs_test_a1ardhex9OzbE4h9DcBZzXxwiZhRAhsukrxN6Os3PHOYcsKquX58VpzHgO",
            "object": "checkout.session",
            "client_reference_id": str(invoice_id),
            "customer": "cus_PDoRlPaff7CDZO",
            "invoice": {
                "id": "in_1OPMoSB5jLfQ2TsFGqEyEFbO",
                "object": "invoice",
                "lines": {
                    "object": "list",
                    "data": [
                        {
                            "id": "il_1OPMoSB5jLfQ2TsFogAM2kw2",
                            "object": "line_item",
                            "price": {
                                "id": "price_1OP91GB5jLfQ2TsFDJ2N2etY",
                                "object": "price",
                                "active": True,
                                "lookup_key": "team-yearly",
                            },
                            "subscription": "sub_1OPMoSB5jLfQ2TsF5Yk9NCeY",
                        }
                    ],
                },
                "paid": True,
                "status": "paid",
                "subscription": "sub_1OPMoSB5jLfQ2TsF5Yk9NCeY",
                "subscription_details": {
                    "metadata": {
                        "invoice_id": str(invoice_id),
                        "subscription_id": str(subscription_id),
                    }
                },
            },
            "mode": "subscription",
            "status": "complete",
            "subscription": {
                "id": "sub_1OPMoSB5jLfQ2TsF5Yk9NCeY",
                "object": "subscription",
                "current_period_end": 1734689740,
                "current_period_start": 1703067340,
                "status": "active",
            },
            "customer_details": {
                "address": {
                    "city": "asf",
                    "country": "AT",
                    "line1": "asfasf",
                    "line2": "asfasf",
                    "postal_code": "asfasf",
                    "state": "asfasf",
                },
                "email": "fabian@chainsquad.com",
                "name": "ChainSquad GmbH",
                "phone": None,
                "tax_exempt": "reverse",
                "tax_ids": [{"type": "eu_vat", "value": "DExxXxXxxxx"}],
            },
        }

    return func


@pytest.fixture()
def setup_team(dbsession, account, create_team):
    team = create_team("private_team")
    billing_repo = repos.InvoiceRepo(dbsession)
    subscriptions = [
        models.Subscription(
            name="Foobar",
            quantity=10,
            price=3000,
            description="Foobar",
            team_id=team.id,
            stripe=models.StripeSubscription(stripe_key="team-yearly"),
        )
    ]
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
    invoice = billing_repo.create(
        models.Invoice(
            user_id=account.id,
            customer=person,
            subscriptions=subscriptions,
        )
    )
    return invoice, team, subscriptions[0]


@pytest.fixture()
def send_webhook(web_client):
    def func(payload, full_session):
        with patch("stripe.checkout.Session.retrieve", return_value=full_session):
            with patch("stripe.Webhook.construct_event", return_value=payload):
                req = web_client.post(
                    "/payment/stripe/webhook",
                    json=payload,
                    auth=("foo", "bar"),
                    headers={"stripe-signature": "foobar"},
                )
        print(req.json())
        req.raise_for_status()
        assert "error" not in req.json()
        return req.json()

    return func


def test_initial_payment(
    dbsession, get_webhook_payload, setup_team, send_webhook, get_get_full_session
):
    invoice, team, subscription = setup_team
    full_session = get_get_full_session(invoice.id, subscription.id)
    webhook_payload = get_webhook_payload(invoice.id)
    send_webhook(webhook_payload, full_session)
    dbsession.commit()
    dbsession.refresh(invoice)
    assert invoice.payment_status == InvoiceStatus.COMPLETED
    dbsession.refresh(team)
    assert team.subscriptions
    subscription = team.subscriptions[0]
    assert subscription.active
    assert subscription.period_starts_at
    assert subscription.period_ends_at

    dbsession.refresh(invoice)
    assert invoice.customer.vat_id == "DExxXxXxxxx"
