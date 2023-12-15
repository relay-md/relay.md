# -*- coding: utf-8 -*-
""" DB Storage models
"""
import enum
import uuid
from datetime import date, datetime
from typing import List

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .user import User


class TeamType(enum.Enum):
    # anyone can view and submit
    PUBLIC = "public"

    # anyone can view, but only some are approved to submit
    RESTRICTED = "restricted"

    # only approved members can view and submit
    PRIVATE = "private"


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
    type: Mapped[TeamType] = mapped_column(Enum(TeamType), default=TeamType.PUBLIC)
    allow_create_topics: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship()  # noqa
    members: Mapped[List["User"]] = relationship(
        secondary="user_team", back_populates="teams"
    )
    topics: Mapped[List["Topic"]] = relationship(  # noqa
        secondary="team_topics", back_populates="teams"
    )

    paid_until: Mapped[date] = mapped_column(Date(), nullable=True)

    @property
    def is_private(self):
        return self.type == TeamType.PRIVATE

    @property
    def is_public(self):
        return self.type == TeamType.PUBLIC

    @property
    def is_restricted(self):
        return self.type == TeamType.RESTRICTED

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    @property
    def is_active(self):
        """Is the team paid? Else, if becomes inactive, no posting, reading
        etc.."""
        # FIXME: needs implementation in API and Teams
        if self.is_public:
            return True
        now = date.today()
        if now < self.paid_until:
            return True
