# -*- coding: utf-8 -*-
""" DB Storage models
"""
import re
import uuid
from datetime import date, datetime
from typing import List

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .permissions import (
    MemberPermissions,
    OwnerPermissions,
    Permissions,
    PublicPermissions,
)
from .user import User
from .user_team import UserTeam

DEFAULT_OWNER_PERMISSIONS = (
    OwnerPermissions.can_read
    | OwnerPermissions.can_post
    | OwnerPermissions.can_modify
    | OwnerPermissions.can_create_topics
    | OwnerPermissions.can_invite
)

DEFAULT_MEMBER_PERMISSIONS = (
    MemberPermissions.can_read
    | MemberPermissions.can_post
    | MemberPermissions.can_modify
    | MemberPermissions.can_create_topics
    | MemberPermissions.can_invite
)

DEFAULT_PUBLIC_PERMISSIONS = PublicPermissions.can_read | PublicPermissions.can_join


class Team(Base):
    """A database model that identifies symbols"""

    __tablename__ = "team"

    #: Unique identifier
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=lambda x: uuid.uuid4(), nullable=False
    )
    name: Mapped[str] = mapped_column(String(32))
    headline: Mapped[str] = mapped_column(String(64), default="", nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    owner_permissions: Mapped[int] = mapped_column(
        default=DEFAULT_OWNER_PERMISSIONS.value
    )
    member_permissions: Mapped[int] = mapped_column(
        default=DEFAULT_MEMBER_PERMISSIONS.value
    )
    public_permissions: Mapped[int] = mapped_column(
        default=DEFAULT_PUBLIC_PERMISSIONS.value
    )

    # Owner
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship()  # noqa
    members: Mapped[List["User"]] = relationship(
        secondary="user_team", back_populates="teams"
    )
    topics: Mapped[List["Topic"]] = relationship(  # noqa
        secondary="team_topics", back_populates="teams"
    )

    paid_until: Mapped[date] = mapped_column(Date(), nullable=True)

    @property
    def is_public(self):
        return self.public_permissions == 0

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    @property
    def can_upgrade(self):
        """Is the team paid? Else, if becomes inactive, no posting, reading
        etc.."""
        return not self.is_paid

    @property
    def is_paid(self):
        """Is the team paid? Else, if becomes inactive, no posting, reading
        etc.."""
        if not self.paid_until:
            return False
        now = date.today()
        if now < self.paid_until:
            return True
        return False

    def can(self, action: Permissions, user: User, membership: UserTeam = None):
        if self.user_id == user.id:
            # owner
            return (action & self.owner_permissions) == action
        if membership:
            # member
            membership_action = membership.can(action)
            if membership_action is not None:
                return membership_action
            return (action & self.member_permissions) == action
        # public
        return (action & self.public_permissions) == action

    @staticmethod
    def validate_team_name(name):
        return re.match("^[\w.-]+$", name)  # noqa
