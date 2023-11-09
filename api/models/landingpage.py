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
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    email: str = Column(String(256))
    confirm_date: datetime = Column(DateTime, default=datetime.utcnow)
