# -*- coding: utf-8 -*-
""" DB Storage models
"""
import enum
import logging
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Column, Enum, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

log = logging.getLogger(__name__)


class OauthProvider(enum.Enum):
    GITHUB = "github"


class User(Base):
    """A database model that identifies symbols"""

    __tablename__ = "user"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    username: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    location: Mapped[str] = mapped_column(String(64), nullable=True)
    oauth_provider: OauthProvider = Column(
        Enum(OauthProvider), default=OauthProvider.GITHUB
    )

    shared_documents: Mapped[List["Document"]] = relationship(  # noqa
        secondary="document_user", back_populates="users"
    )
    owned_documents: Mapped[List["Document"]] = relationship(  # noqa
        back_populates="user"
    )
    teams: Mapped[List["Team"]] = relationship(  # noqa
        secondary="user_team", back_populates="members"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: @{str(self.username)}>"


Index("user_oauth_index", User.username, User.oauth_provider)
