# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class TeamTopic(Base):
    __tablename__ = "team_topics"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team.id"))
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topic.id"))

    # If needed, we habe to look for SA warnings caused by those.
    # viewonly surpresses the warnings
    team: Mapped["Team"] = relationship(viewonly=True)  # noqa
    topic: Mapped["Topic"] = relationship(viewonly=True)  # noqa

    @hybrid_property
    def name(self):
        return str(self)

    def __str__(self):
        return f"{self.topic.name}@{self.team.name}"

    def __repr__(self):
        return f"<{self.__class__.__name__}@{self.topic.name} in {self.team.name}>"
