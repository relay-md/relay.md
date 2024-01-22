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

from ..config import get_config
from ..database import Base

log = logging.getLogger(__name__)


class OauthProvider(enum.Enum):
    GITHUB = "github"
    GOOGLE = "google"


class User(Base):
    """A database model that identifies symbols"""

    __tablename__ = "user"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    username: Mapped[str] = mapped_column(String(256), unique=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    oauth_provider: OauthProvider = Column(
        Enum(OauthProvider), default=OauthProvider.GITHUB
    )
    profile_picture_url: Mapped[str] = mapped_column(String(255), nullable=True)

    shared_documents: Mapped[List["Document"]] = relationship(  # noqa
        secondary="document_user", back_populates="users"
    )
    owned_documents: Mapped[List["Document"]] = relationship(  # noqa
        back_populates="user"
    )
    owned_assets: Mapped[List["Asset"]] = relationship(back_populates="user")  # noqa
    teams: Mapped[List["Team"]] = relationship(  # noqa
        secondary="user_team", back_populates="members"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: @{str(self.username)}>"

    @property
    def is_admin(self):
        return str(self.id) in get_config().ADMIN_USER_IDS


Index("user_oauth_index_unique", User.username, User.oauth_provider, unique=True)
