# -*- coding: utf-8 -*-
""" DB Storage models
"""
import logging
import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base

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
