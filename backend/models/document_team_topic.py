# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class DocumentTeamTopic(Base):
    __tablename__ = "document_team_topics"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document.id"))
    team_topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("team_topics.id"))

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
