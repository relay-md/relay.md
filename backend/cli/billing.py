# -*- coding: utf-8 -*-

from uuid import UUID

import click
from rich.console import Console

from .. import models, repos
from ..database import get_session

console = Console()


@click.group()
def billing():
    pass


@billing.command()
@click.argument("email")
def demo(email):
    (db,) = get_session()
    billing_repo = repos.InvoiceRepo(db)
    user = repos.UserRepo(db).get_by_kwargs(email=email)
    if not user:
        raise ValueError("User not found")
    subscriptions = [
        models.Subscription(
            name="Foobar", quantity=10, price=3000, description="Team subscription"
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
    invoice = models.Invoice(
        user_id=user.id,
        customer=person,
        subscriptions=subscriptions,
    )

    invoice_db = billing_repo.create(invoice)
    console.print(invoice_db)
    console.print(invoice_db.id)
    # console.print(billing_repo.get_payment_session(invoice))
    console.print(billing_repo.get_payment_link(invoice))


@billing.command()
@click.argument("invoice_id", type=UUID)
def claim(invoice_id: UUID):
    db = next(get_session())
    invoice_repo = repos.InvoiceRepo(db)
    invoice = invoice_repo.get_by_id(invoice_id)
    if not invoice:
        raise ValueError("Unknown Invoice")
    console.print(invoice_repo.subscription_payment(invoice))


@billing.command()
@click.argument("invoice_id", type=UUID)
def authorize(invoice_id: UUID):
    webhook = {
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
                    "merchantReference": str(invoice_id),
                    "pspReference": "ZCLWCV5MP8JSTC82",
                    "reason": "1234:7777:12/2012",
                    "success": "true",
                }
            }
        ],
    }

    import logging

    logging.basicConfig(level=logging.DEBUG)
    db = next(get_session())
    invoice_repo = repos.InvoiceRepo(db)
    print(invoice_repo.process_webhook(webhook))
