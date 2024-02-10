# -*- coding: utf-8 -*-
""" DB Storage models
"""
import re
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .permissions import Permissions
from .user import User
from .user_team import UserTeam

DEFAULT_OWNER_PERMISSIONS = (
    Permissions.can_read
    | Permissions.can_post
    | Permissions.can_modify
    | Permissions.can_create_topics
    | Permissions.can_invite
    | Permissions.can_join
)

DEFAULT_MEMBER_PERMISSIONS = (
    Permissions.can_read
    | Permissions.can_post
    | Permissions.can_modify
    | Permissions.can_create_topics
    | Permissions.can_invite
)

DEFAULT_PUBLIC_PERMISSIONS = (
    Permissions.can_read
    | Permissions.can_post
    | Permissions.can_create_topics
    | Permissions.can_join
)


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
    subscriptions: Mapped[List["Subscription"]] = relationship(  # noqa
        back_populates="team"
    )

    seats: Mapped[int] = mapped_column(Integer(), default=5)

    # Should this be shown in directory listing teams?
    hide: Mapped[bool] = mapped_column(default=False)
    favorit: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    @property
    def active_subscription(self):
        """Return the active subscription"""
        for subscription in self.subscriptions:
            if subscription.active:
                return subscription

    def can(
        self, action: Permissions, user: User, membership: Optional[UserTeam] = None
    ):
        if not user:
            return False
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
        return bool((action & self.public_permissions) == action)

    @staticmethod
    def validate_team_name(name):
        return re.match("^[\w.-]+$", name)  # noqa
