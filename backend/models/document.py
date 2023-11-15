# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .team_topic import TeamTopic


class Document(Base):
    """A database model that identifies symbols"""

    __tablename__ = "document"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    filename: Mapped[str] = mapped_column(String(length=256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    team_topics: Mapped[List[TeamTopic]] = relationship(
        secondary="document_team_topics"
    )

    @property
    def is_private(self):
        # TODO: Needs implemtation using team_topics
        return False
