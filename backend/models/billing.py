# -*- coding: utf-8 -*-
""" DB Storage modat"""
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class ProductInformation(Base):
    __tablename__ = "billing_product"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    name: Mapped[str] = mapped_column(String(64))
    quantity: Mapped[int] = mapped_column()
    price: Mapped[int] = mapped_column()

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, quantity={self.quantity}, price={self.price})"


class PersonalInformation(Base):
    __tablename__ = "billing_person"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
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


class PaymentPlan(Base):
    __tablename__ = "billing_payment_plan"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    days_between_payments: Mapped[int] = mapped_column()
    expiry: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        return f"{self.__class__.__name__}(days_between_payments={self.days_between_payments})"


class InvoiceProducts(Base):
    __tablename__ = "billing_invoice_products"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("billing_invoice.id"))
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("billing_product.id"))


class Invoice(Base):
    __tablename__ = "billing_invoice"

    # Used as payment reference
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("billing_person.id"))
    payment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("billing_payment_plan.id"))
    customer: Mapped[PersonalInformation] = relationship()
    payment: Mapped[PaymentPlan] = relationship()
    products: Mapped[List[ProductInformation]] = relationship(
        secondary="billing_invoice_products"
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(customer={self.customer},products={self.products}, payment={self.payment})"
