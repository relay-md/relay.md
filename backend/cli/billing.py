# -*- coding: utf-8 -*-

import click
from rich import print
from rich.console import Console

from .. import repos, schema

console = Console()


@click.group()
def billing():
    pass


@billing.command()
def demo():
    billing_repo = repos.CheckoutComBillingRepo()
    products = [
        schema.BillingProductInformation(name="Foobar", quantity=10, price=3000)
    ]
    person = schema.BillingPersonalInformation(
        name="Fabian Schuh",
        email="fabian@chainsquad.com",
        address_line1="Address 13, 24 Foobar",
        city="Erlangen",
        state="Bavaria",
        zip="91058",
        country="DE",
        phone_country_code="+49",
        phone_number="1706397354",
    )
    payment_plan = schema.BillingRecurringPaymentPlan(
        days_between_payments=30, expiry="20261231"
    )

    print(billing_repo.get_payment_link(person, products, payment_plan))
