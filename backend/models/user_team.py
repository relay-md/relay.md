# -*- coding: utf-8 -*-
""" Memberships and permissions for teams
"""
import uuid

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class UserTeam(Base):
    __tablename__ = "user_team"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team.id"))

    user: Mapped["User"] = relationship(viewonly=True)  # noqa
    team: Mapped["Team"] = relationship(viewonly=True)  # noqa

    can_invite_users: Mapped[bool] = mapped_column(default=False)
    can_post_documents: Mapped[bool] = mapped_column(default=False)
    can_delete_documents: Mapped[bool] = mapped_column(default=False)
    can_modify_documents: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


Index("user_team_idx_unique", UserTeam.user_id, UserTeam.team_id, unique=True)
