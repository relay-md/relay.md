# -*- coding: utf-8 -*-
""" DB Storage models
"""
import logging
import uuid
from typing import List
import enum

from sqlalchemy import String, func, select
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    and_,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, Session

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
