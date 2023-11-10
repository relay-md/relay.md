# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class LandingPageEmail(Base):
    """The general User Storage class"""

    __tablename__ = "landing_emails"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, nullable=False
    )
    email: str = Column(String(256))
    created_date: datetime = Column(DateTime, default=datetime.utcnow)
    confirm_token: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4)
    confirm_date: datetime = Column(DateTime, nullable=True)

    def confirm(self, token: str) -> None:
        if self.confirm_token != uuid.UUID(token):
            raise ValueError("Confirm code is invalid")
