# -*- coding: utf-8 -*-
""" DB Storage models
"""
import logging
import uuid
from typing import List
import enum

from sqlalchemy import String, func, select
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

log = logging.getLogger(__name__)


class Document(Base):
    """A database model that identifies symbols"""

    __tablename__ = "document"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    filename: Mapped[str] = mapped_column(String(length=256))
