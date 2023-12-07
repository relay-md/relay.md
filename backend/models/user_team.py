# -*- coding: utf-8 -*-
""" Memberships and permissions for teams
"""
import uuid

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class UserTeam(Base):
    __tablename__ = "user_team"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team.id"))

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


Index("user_team_idx", UserTeam.user_id, UserTeam.team_id)
