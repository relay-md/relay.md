# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class DocumentAccess(Base):
    __tablename__ = "document_access"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document.id"))
    access_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"<{self.__class__.__name__}@{self.user.username}>"
