# -*- coding: utf-8 -*-
""" DB Storage models
"""
import logging
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

log = logging.getLogger(__name__)


class AccessToken(Base):
    """A database model that identifies symbols"""

    __tablename__ = "access_token"

    #: Unique identifier
    token: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(backref="access_tokens")  # noqa

    latest_document_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime(2020, 1, 1)
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}@{self.user.username}>"
