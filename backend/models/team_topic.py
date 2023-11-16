# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class TeamTopic(Base):
    __tablename__ = "team_topics"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team.id"))
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topic.id"))

    team: Mapped["Team"] = relationship()  # noqa
    topic: Mapped["Topic"] = relationship()  # noqa

    @property
    def name(self):
        return str(self)

    def __str__(self):
        return f"{self.topic.name}@{self.team.name}"