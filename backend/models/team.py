# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Team(Base):
    """A database model that identifies symbols"""

    __tablename__ = "team"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    name: Mapped[str] = mapped_column(String(32))
    # TODO: add a description to teams for the overview
    # description: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Owner
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    is_private: Mapped[bool] = mapped_column(default=False)
    allow_create_topics: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship()  # noqa

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"
