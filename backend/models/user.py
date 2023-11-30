# -*- coding: utf-8 -*-
""" DB Storage models
"""
import enum
import logging
import uuid
from datetime import datetime

from sqlalchemy import Column, Enum, Index, String
from sqlalchemy.orm import Mapped, mapped_column

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


Index("user_oauth_index", User.username, User.oauth_provider)
