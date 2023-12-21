# -*- coding: utf-8 -*-
""" DB Storage modat"""
import enum
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .user import User


class InvoiceStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    EXPIRED = "expired"


class OrderItem(Base):
    __tablename__ = "billing_product"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    # Reference to the invoice
    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("billing_invoice.id"))

    # E.g. Team Subscription
    name: Mapped[str] = mapped_column(String(64))
    # E.g. Name
    description: Mapped[str] = mapped_column(String(64))
    quantity: Mapped[int] = mapped_column()
    price: Mapped[int] = mapped_column()

    # In case this pays for a team, we link the team here
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team.id"), nullable=True)
    team: Mapped["Team"] = relationship()  # noqa

    # Internal id for corresponding stripe product
    stripe_key: Mapped[str] = mapped_column(String(32))

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, quantity={self.quantity}, price={self.price})"


class PersonalInformation(Base):
    __tablename__ = "billing_person"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )

    # TODO: at some point, we want to link this to the user so we can present it
    # when changing subscription
    #
    # user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    # user: Mapped[User] = relationship()

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
    phone_country_code: Mapped[str] = mapped_column(String(6))
    phone_number: Mapped[str] = mapped_column(String(128))

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
    payment_failure_reason: Mapped[str] = mapped_column(Text(), nullable=True)

    payment_provider_reference: Mapped[str] = mapped_column(String(256), nullable=True)

    paid_at: Mapped[datetime] = mapped_column(nullable=True)

    user: Mapped[User] = relationship()
    customer: Mapped[PersonalInformation] = relationship()
    products: Mapped[List[OrderItem]] = relationship()

    def __repr__(self):
        return f"{self.__class__.__name__}(customer={self.customer},products={self.products})"

    @property
    def total_amount(self):
        return sum([x.quantity * x.price for x in self.products])
