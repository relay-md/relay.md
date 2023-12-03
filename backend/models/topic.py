# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Topic(Base):
    """A database model that identifies symbols"""

    __tablename__ = "topic"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    name: Mapped[str] = mapped_column(String(32))

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"
