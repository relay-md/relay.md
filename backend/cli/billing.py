# -*- coding: utf-8 -*-

from datetime import date

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
    products = [models.ProductInformation(name="Foobar", quantity=10, price=3000)]
    person = models.PersonalInformation(
        user_id=user.id,
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
        customer=person,
        products=products,
        payment=payment_plan,
    )

    invoice_db = billing_repo.create(invoice)
    console.print(invoice_db)
    console.print(invoice_db.id)
    console.print(billing_repo.get_payment_link(invoice))
