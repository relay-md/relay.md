# -*- coding: utf-8 -*-
""" DB Storage modat"""
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import CHAR, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .team_topic import TeamTopic
from .user import User


class Document(Base):
    """A database model that identifies symbols"""

    __tablename__ = "document"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )

    title: Mapped[str] = mapped_column(String(256), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    filename: Mapped[str] = mapped_column(String(length=256))

    filesize: Mapped[int] = mapped_column(BigInteger(), nullable=True)
    checksum_sha256: Mapped[str] = mapped_column(String(length=64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    team_topics: Mapped[List[TeamTopic]] = relationship(
        secondary="document_team_topics"
    )
    users: Mapped[List[User]] = relationship(secondary="document_user")
    user: Mapped["User"] = relationship(back_populates="owned_documents")  # noqa

    embeds: Mapped[List["Asset"]] = relationship(back_populates="document")  # noqa

    # if this is set, the document can be viewed online by anyone on the web
    # viewer, this will be automatically set when uploading a document. For
    # instance, when sending a doc to the `_` team.
    is_public: Mapped[bool] = mapped_column(default=False)

    # 128bit password hash, as bytes TODO: needs implementation
    read_password_hash: Mapped[bytes] = mapped_column(CHAR(32), default=b"")

    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}@{self.user.username}>"

    @property
    def shared_with(self):
        return [x.name for x in self.team_topics] + [
            f"@{x.username}" for x in self.users
        ]
