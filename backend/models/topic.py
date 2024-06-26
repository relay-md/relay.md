# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Topic(Base):
    """A database model that identifies symbols"""

    __tablename__ = "topic"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    name: Mapped[str] = mapped_column(String(32))
    teams: Mapped[List["Team"]] = relationship(  # noqa
        secondary="team_topics", back_populates="topics"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"
