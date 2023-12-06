# -*- coding: utf-8 -*-
""" Subscriptions of a user into a team topic
"""
import uuid

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class UserTeamTopic(Base):
    __tablename__ = "user_team_topics"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    team_topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team_topics.id"))

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


Index("user_team_topics_idx", UserTeamTopic.user_id, UserTeamTopic.team_topic_id)
