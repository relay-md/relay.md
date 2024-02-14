# -*- coding: utf-8 -*-
import logging

import click
import stripe as STRIPE
from rich import print
from rich.console import Console

from backend.config import get_config

console = Console()
log = logging.getLogger(__name__)
config = get_config()


@click.group()
def stripe():
    pass


@stripe.command()
@click.argument("url")
def webhook(url):
    STRIPE.api_key = config.STRIPE_API_PRIVATE_KEY
    url = f"https://foo:bar@{url}/payment/stripe/webhook"
    print(f"Installing new endpoint: {url}")
    print(
        STRIPE.WebhookEndpoint.create(
            enabled_events=[
                "invoice.payment_failed",
                "invoice.paid",
                "customer.subscription.pending_update_expired",
                "customer.subscription.pending_update_applied",
                "customer.subscription.deleted",
                "customer.subscription.created",
                "checkout.session.completed",
            ],
            url=url,
        )
    )
