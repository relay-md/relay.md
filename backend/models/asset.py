# -*- coding: utf-8 -*-
""" DB Storage modat"""
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .user import User


class Asset(Base):
    """A database model that identifies symbols"""

    __tablename__ = "asset"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document.id"))
    filename: Mapped[str] = mapped_column(String(length=256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user: Mapped["User"] = relationship(back_populates="owned_assets")  # noqa

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.filename}>"
