# -*- coding: utf-8 -*-
""" Memberships and permissions for teams
"""
import uuid

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .permissions import Permissions


class UserTeam(Base):
    __tablename__ = "user_team"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team.id"))

    user: Mapped["User"] = relationship(viewonly=True)  # noqa
    team: Mapped["Team"] = relationship(viewonly=True)  # noqa

    # None means the parent (team) permissions are relevant.
    permissions: Mapped[int] = mapped_column(nullable=True, default=None)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def can(self, action: Permissions):
        if self.permissions:
            return (action & self.permissions) == action
        # will be checked further on team.py
        return None


Index("user_team_idx_unique", UserTeam.user_id, UserTeam.team_id, unique=True)
