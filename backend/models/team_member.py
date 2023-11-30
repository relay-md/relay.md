# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class TeamMember(Base):
    __tablename__ = "team_member"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    team: Mapped["Team"] = relationship()  # noqa
    user: Mapped["User"] = relationship()  # noqa

    # Owns a team
    is_owner: Mapped[bool] = mapped_column(default=False)

    # can moderate a team
    is_moderator: Mapped[bool] = mapped_column(default=False)
