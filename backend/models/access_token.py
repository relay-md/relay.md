# -*- coding: utf-8 -*-
""" DB Storage models
"""
import logging
import uuid

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
