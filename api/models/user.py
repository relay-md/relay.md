# -*- coding: utf-8 -*-
""" DB Storage models
"""
import enum
import logging
import uuid

from sqlalchemy import Column, Enum, String
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

    username: Mapped[str] = mapped_column(String(256))
    oauth_provider: OauthProvider = Column(Enum(OauthProvider))
