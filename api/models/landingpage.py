import enum
import logging
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    and_,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base, Session


class LandingPageEmail(Base):
    """The general User Storage class"""

    __tablename__ = "landing_emails"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    email : str = Column(String(256))
    confirm_date: datetime = Column(DateTime, default=datetime.utcnow)
