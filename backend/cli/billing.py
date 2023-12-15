# -*- coding: utf-8 -*-

from datetime import date
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
    products = [
        models.OrderItem(
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
    payment_plan = models.PaymentPlan(
        days_between_payments=30, expiry=date(2025, 12, 31)
    )
    invoice = models.Invoice(
        user_id=user.id,
        customer=person,
        products=products,
        payment=payment_plan,
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
