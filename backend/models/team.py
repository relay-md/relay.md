# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Team(Base):
    """A database model that identifies symbols"""

    __tablename__ = "team"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    name: Mapped[str] = mapped_column(String(32))

    # TODO: add an is_private flag
