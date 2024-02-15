# -*- coding: utf-8 -*-
import abc
import logging
from datetime import datetime
from uuid import UUID

import stripe
from sqlalchemy import select

from ..config import get_config
from ..models.billing import (
    Invoice,
    InvoiceStatus,
    PersonalInformation,
    Subscription,
)
from .base import DatabaseAbstractRepository
from .mautic import MauticRepo
from .stripe import (
    StripeCustomerRepo,
    StripeSubscription,
    StripeSubscriptionRepo,
)

log = logging.getLogger(__name__)


class AbstractPaymentGateway:
    @abc.abstractmethod
    def get_payment_session(self, invoice: Invoice):
        pass

    @abc.abstractmethod
    async def process_webhook(self, request):
        pass


class StripePayments(AbstractPaymentGateway):
    def __init__(self):
        stripe.api_key = get_config().STRIPE_API_PRIVATE_KEY

    def get_payment_session(self, invoice: Invoice):
        customer = invoice.customer
        line_items = list()
        for item in invoice.subscriptions:
            prices = stripe.Price.list(
                lookup_keys=[item.stripe.stripe_key], expand=["data.product"]
            )
            line_items.append(
                {
                    "price": prices.data[0].id,
                    "quantity": item.quantity,
                },
            )

        session_create_params = dict(
            client_reference_id=str(invoice.id),
            currency="EUR",
            customer=customer.stripe.stripe_customer_id,
            line_items=line_items,
            mode="subscription",
            success_url=f"{get_config().STRIPE_RETURN_URL_SUCCESS}",  # ?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=get_config().STRIPE_RETURN_URL_CANCEL,
            subscription_data=dict(
                metadata=dict(
                    invoice_id=str(invoice.id),
                    team_id=invoice.subscriptions[0].team_id,
                    subscription_id=invoice.subscriptions[0].id,
                )
            ),
            # Promo codes should be enterable on checkout page. This enables
            # promo-codes from stripe pov and needs no further implementation on
            # relay.md side!
            allow_promotion_codes=True,
            # proration_behavior="always_invoice",
            # We want stripe to deal with tax
            automatic_tax=dict(enabled=True),
        )
        if customer.is_business:
            session_create_params.update(
                dict(
                    tax_id_collection=dict(enabled=True),
                    customer_update=dict(name="auto"),
                )
            )

        # https://stripe.com/docs/api/checkout/sessions/create
        checkout_session = stripe.checkout.Session.create(**session_create_params)
        return checkout_session

    async def process_webhook(self, db, request):
        sig_header = request.headers["stripe-signature"]
        try:
            event = stripe.Webhook.construct_event(
                await request.body(), sig_header, get_config().STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        # Some documentation about subscriptions and webhook on stripe
        # https://stripe.com/docs/billing/subscriptions/webhooks
        #
        log.info(f"Webhook received: {event['type']}")

        # Payment specficif webhook ####################################
        # https://stripe.com/docs/api/checkout/sessions/object
        ################################################################
        if event["type"] == "checkout.session.completed":
            # Repos
            invoice_repo = InvoiceRepo(db)
            subscription_repo = SubscriptionRepo(db)
            person_repo = PersonalInformationRepo(db)

            # Get the full session with subscription
            session = stripe.checkout.Session.retrieve(
                event["data"]["object"]["id"],
                expand=["subscription", "invoice", "customer"],
            )
            stripe_invoice = session["invoice"]
            stripe_subscription = session["subscription"]
            invoice_id = session["client_reference_id"]
            subscription_id = stripe_invoice["subscription_details"]["metadata"][
                "subscription_id"
            ]

            local_invoice = invoice_repo.get_by_id(invoice_id)
            if not local_invoice:
                from ..exceptions import BadRequest

                raise BadRequest("Invalid invoice ID")
            invoice_repo.succeed_invoice_payment(local_invoice)

            # store subscription id
            stripe_subscription_id = stripe_invoice["subscription"]

            local_subscription = subscription_repo.get_by_id(UUID(subscription_id))
            if not local_subscription:
                raise ValueError("No corresponding subscription locally!?")

            subscription_repo.store_subscription_id(
                local_subscription, stripe_subscription_id
            )

            # Update subscription
            start_date = datetime.utcfromtimestamp(
                session["subscription"]["current_period_start"]
            )
            end_date = datetime.utcfromtimestamp(
                session["subscription"]["current_period_end"]
            )
            active = stripe_subscription["status"] == "active"
            subscription_repo.update(
                local_subscription,
                active=active,
                period_starts_at=start_date,
                period_ends_at=end_date,
            )

            from rich import print

            print(session)

            # Update the customer / vat id
            customer_details = session.get("customer_details", {})
            tax_ids = customer_details.get("tax_ids")
            if tax_ids:
                # use just the first one
                tax_id = tax_ids[0]["value"]
                person_repo.update(local_invoice.customer, vat_id=tax_id)

        # Invoice specific webhooks ####################################
        # https://stripe.com/docs/api/invoices/object
        ################################################################
        elif event["type"] in ["invoice.paid", "invoice.payment_failed"]:
            stripe_invoice = event["data"]["object"]

            invoice_repo = InvoiceRepo(db)
            subscription_repo = SubscriptionRepo(db)

            stripe_subscription_id = stripe_invoice["subscription"]
            invoice_id = stripe_invoice["subscription_details"]["metadata"][
                "invoice_id"
            ]
            subscription_id = stripe_invoice["subscription_details"]["metadata"][
                "subscription_id"
            ]

            subscription = subscription_repo.get_by_id(subscription_id)
            if not subscription:
                raise ValueError("No corresponding subscription locally!?")
            subscription_repo.store_subscription_id(
                subscription, stripe_subscription_id
            )
            subscription_repo.update(subscription, active=stripe_invoice["paid"])

            invoice = invoice_repo.get_by_id(invoice_id)
            if not invoice:
                from ..exceptions import BadRequest

                raise BadRequest("Invalid invoice ID")

            if stripe_invoice["paid"]:
                invoice_repo.succeed_invoice_payment(invoice)

        # Subscription specific webhook ################################
        # https://stripe.com/docs/api/subscriptions/object
        ################################################################
        elif event["type"] == "customer.subscription.updated":
            stripe_subscription = event["data"]["object"]
            subscription_repo = SubscriptionRepo(db)
            subscription_id = stripe_subscription["metadata"]["subscription_id"]
            subscription = subscription_repo.get_by_id(subscription_id)
            if not subscription:
                raise ValueError("No corresponding subscription locally!?")

            invoice_id = stripe_subscription["metadata"]["invoice_id"]
            # we only process the first item because only have one!
            item = stripe_subscription["items"]["data"][0]
            stripe_subscription_id = item["subscription"]
            subscription_repo.store_subscription_id(
                subscription, stripe_subscription_id
            )

            lookup_key = item["price"]["lookup_key"]
            quantity = item["quantity"]
            if lookup_key == "team_yearly":
                price = get_config().PRICING_TEAM_YEARLY
            else:
                price = get_config().PRICING_TEAM_MONTHLY
            # Update subscription
            start_date = datetime.utcfromtimestamp(
                stripe_subscription["current_period_start"]
            )
            end_date = datetime.utcfromtimestamp(
                stripe_subscription["current_period_end"]
            )
            subscription_repo.update(
                subscription,
                price=price,
                quantity=quantity,
                active=stripe_subscription["status"] == "active",
                period_starts_at=start_date,
                period_ends_at=end_date,
            )

            # TODO: we'll want to make a check on the front end to see if the
            # subscription is past due and then prompt the user to update their
            # payment method
            if stripe_subscription.get("status") == "past_due":
                subscription_repo.update(
                    subscription,
                    active=False,
                    period_ends_at=datetime.utcnow(),
                )

            # TODO: Stripe will send a subscription.updated event when a subscription is canceled
            # but the subscription is still active until the end of the period.
            # So we check if cancel_at_period_end is true and send an email to the customer.
            # https://stripe.com/docs/billing/subscriptions/cancel#events
            if stripe_subscription.get("cancel_at_period_end"):
                # mail: subject: 'We hate to see you go :(',
                pass

        elif event["type"] == "customer.subscription.created":
            stripe_subscription = event["data"]["object"]
            subscription_repo = SubscriptionRepo(db)
            subscription_id = stripe_subscription["metadata"]["subscription_id"]
            subscription = subscription_repo.get_by_id(subscription_id)
            if not subscription:
                raise ValueError("No corresponding subscription locally!?")

            subscription_repo.store_subscription_id(
                subscription, stripe_subscription["id"]
            )

        elif event["type"] == "customer.subscription.deleted":
            stripe_subscription = event["data"]["object"]
            subscription_repo = SubscriptionRepo(db)
            subscription_id = stripe_subscription["metadata"]["subscription_id"]
            subscription = subscription_repo.get_by_id(subscription_id)
            if not subscription:
                raise ValueError("No corresponding subscription locally!?")

            subscription_repo.update(subscription, active=False)

        # Fallback
        ################################################################
        else:
            log.error("Unhandled event type {}".format(event["type"]))


class InvoiceRepo(DatabaseAbstractRepository):
    ORM_Model = Invoice

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment = StripePayments()

    def get_payment_session(self, invoice: Invoice):
        return self.payment.get_payment_session(invoice)

    async def process_webhook(self, request):
        return await self.payment.process_webhook(self._db, request)

    def succeed_invoice_payment(self, invoice: Invoice):
        log.info(f"Invoice {invoice.id} was just paid successfully")
        # update each subscription if neede
        return self.update(
            invoice, payment_status=InvoiceStatus.COMPLETED, paid_at=datetime.utcnow()
        )


class SubscriptionRepo(DatabaseAbstractRepository):
    ORM_Model = Subscription

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment = StripePayments()

    def store_in_mautic(self, subscription: Subscription):
        mautic_repo = MauticRepo()
        mautic_repo.process_subscription(subscription)

    def update(self, item: Subscription, **kwargs):
        old_active = item.active
        new_active = kwargs.get("active", item.active)
        super().update(item, **kwargs)
        if old_active != new_active:
            self.store_in_mautic(item)

    def store_subscription_id(self, subscription: Subscription, id):
        stripe_subscription_repo = StripeSubscriptionRepo(self._db)
        stripe_subscription = stripe_subscription_repo.get_by_kwargs(
            subscription_id=subscription.id
        )
        stripe_subscription_repo.update(stripe_subscription, stripe_subscription_id=id)

    def cancel_subscription(self, subscription: Subscription):
        self.update(subscription, active=False)
        if not subscription.stripe:
            log.error(f"Subscription {subscription.id} has no relation to stripe!")
            return subscription
        stripe.Subscription.modify(
            subscription.stripe.stripe_subscription_id,
            cancel_at_period_end=True,
        )

    def update_quantity(self, subscription: Subscription, new_quantity):
        self.update(subscription, quantity=new_quantity)

        if not subscription.stripe or not subscription.stripe.stripe_subscription_id:
            log.error(f"Subscription {subscription.id} has no relation to stripe!")
            return subscription

        subscription_items = stripe.SubscriptionItem.list(
            subscription=subscription.stripe.stripe_subscription_id, limit=1
        )
        assert subscription_items["data"]
        subscription_item = subscription_items["data"][0]
        stripe.SubscriptionItem.modify(
            subscription_item["id"],
            quantity=new_quantity,
        )
        return subscription

    def get_latest_subscription_for_team_id(self, team_id: UUID):
        return self._db.scalar(
            select(Subscription)
            .filter_by(team_id=team_id)
            .order_by(Subscription.created_at.desc())
        )

    def get_subscription_from_stripe_id(self, stripe_id):
        stripe_subscription = self._db.scalar(
            select(StripeSubscription).filter_by(stripe_subscription_id=stripe_id)
        )
        if stripe_subscription:
            return stripe_subscription.subscription


class PersonalInformationRepo(DatabaseAbstractRepository):
    ORM_Model = PersonalInformation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment = StripePayments()

    def get_stripe_customer_payload(self, personal_info: PersonalInformation, ip: str):
        customer_create_payload = dict(
            name=personal_info.name,
            email=personal_info.user.email,
            address=dict(
                city=personal_info.city,
                country=personal_info.country_code,
                line1=personal_info.address_line1,
                line2=personal_info.address_line2,
                postal_code=personal_info.zip,
                state=personal_info.state,
            ),
            tax=dict(ip_address=ip),
        )
        return customer_create_payload

    def create_from_kwargs(self, **kwargs):
        ip = kwargs.pop("ip", None)
        personal_info: PersonalInformation = super().create_from_kwargs(**kwargs)

        # Create Stripe customer
        # https://docs.stripe.com/api/customers/create
        customer_create_payload = self.get_stripe_customer_payload(personal_info, ip)
        stripe_customer = stripe.Customer.create(**customer_create_payload)
        stripe_customer_repo = StripeCustomerRepo(self._db)
        stripe_customer_repo.create_from_kwargs(
            personal_information_id=personal_info.id,
            stripe_customer_id=stripe_customer["id"],
        )
        self.store_in_mautic(personal_info)
        return personal_info

    def store_in_mautic(self, personal_info: PersonalInformation):
        mautic_repo = MauticRepo()
        mautic_repo.process_person(personal_info)

    def update(self, personal_info, **kwargs):
        ip = kwargs.pop("ip", None)
        super().update(personal_info, **kwargs)

        customer_repo = StripeCustomerRepo(self._db)
        customer = customer_repo.get_by_kwargs(personal_information_id=personal_info.id)
        if not customer:
            log.error(
                "No stripe customer id known for PersonalInformation {personal_info.id}. Skipping updating Stripe..."
            )
            return personal_info

        customer_create_payload = self.get_stripe_customer_payload(personal_info, ip)
        # https://docs.stripe.com/api/customers/update
        stripe.Customer.modify(
            customer.stripe_customer_id,
            **customer_create_payload,
        )
        self.store_in_mautic(personal_info)
        return personal_info
