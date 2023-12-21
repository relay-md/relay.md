# -*- coding: utf-8 -*-
import logging
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base

log = logging.getLogger(__name__)


class StripeCustomer(Base):
    __tablename__ = "stripe_customer"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    personal_information_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("billing_person.id")
    )
    stripe_customer_id: Mapped[str] = mapped_column(String(32))


class StripeSubscription(Base):

    __tablename__ = "stripe_subscription"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    subscription_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("billing_subscription.id"), unique=True
    )

    # Internal id for corresponding stripe product
    stripe_key: Mapped[str] = mapped_column(String(32))
    stripe_subscription_id: Mapped[str] = mapped_column(String(32), nullable=True)
