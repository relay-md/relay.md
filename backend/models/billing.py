# -*- coding: utf-8 -*-
""" DB Storage modat"""
import enum
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import get_config
from ..database import Base
from .user import User


class InvoiceStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    EXPIRED = "expired"


class Subscription(Base):
    __tablename__ = "billing_subscription"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    # Reference to the invoice
    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("billing_invoice.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    # E.g. Team Subscription
    name: Mapped[str] = mapped_column(String(64))
    # E.g. Name
    description: Mapped[str] = mapped_column(String(64))
    # e.g. number of team members!
    quantity: Mapped[int] = mapped_column()
    price: Mapped[int] = mapped_column()

    # The subscription is active?
    active: Mapped[bool] = mapped_column(default=False)

    # In case this pays for a team, we link the team here
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team.id"), nullable=True)
    team: Mapped["Team"] = relationship(back_populates="subscriptions")  # noqa

    invoice: Mapped["Invoice"] = relationship(back_populates="subscriptions")  # noqa
    stripe: Mapped["StripeSubscription"] = relationship(  # noqa
        back_populates="subscription"
    )

    period_starts_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    period_ends_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    @property
    def is_yearly(self):
        if self.price == int(get_config().PRICING_TEAM_YEARLY * 100):
            return True
        return False

    @property
    def is_monthly(self):
        return not self.is_yearly

    @property
    def user(self):
        return self.invoice.user

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, quantity={self.quantity}, price={self.price})"


class PersonalInformation(Base):
    __tablename__ = "billing_person"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship()

    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128))
    # Address
    address_line1: Mapped[str] = mapped_column(String(128))
    address_line2: Mapped[str] = mapped_column(String(128), nullable=True)
    city: Mapped[str] = mapped_column(String(128))
    state: Mapped[str] = mapped_column(String(128))
    zip: Mapped[str] = mapped_column(String(128))
    country_code: Mapped[str] = mapped_column(String(3))
    # Phone
    phone_country_code: Mapped[str] = mapped_column(String(6), default="")
    phone_number: Mapped[str] = mapped_column(String(128), default="")

    stripe: Mapped["StripeCustomer"] = relationship()  # noqa

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, email={self.email})"


class Invoice(Base):
    __tablename__ = "billing_invoice"

    # Used as payment reference
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("billing_person.id"))
    payment_status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus), default=InvoiceStatus.PENDING
    )

    paid_at: Mapped[datetime] = mapped_column(nullable=True)

    user: Mapped[User] = relationship()
    customer: Mapped[PersonalInformation] = relationship()
    subscriptions: Mapped[List[Subscription]] = relationship()

    def __repr__(self):
        return f"{self.__class__.__name__}(customer={self.customer},subscriptions={self.subscriptions})"

    @property
    def total_amount(self):
        return sum([x.quantity * x.price for x in self.subscriptions])
