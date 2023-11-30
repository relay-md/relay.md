# -*- coding: utf-8 -*-
""" DB Storage models
"""
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class DocumentUser(Base):
    __tablename__ = "document_user"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
