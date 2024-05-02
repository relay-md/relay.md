# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID

from sqlalchemy import and_

from ..models.user import User
from ..models.team import Team
from ..models.user_team import UserTeam
from ..models.team_topic import TeamTopic
from ..models.user_team_topic import UserTeamTopic
from .base import DatabaseAbstractRepository


class UserTeamRepo(DatabaseAbstractRepository):
    ORM_Model = UserTeam

    def add_member(self, user: User, team: Team):
        self.create_from_kwargs(user_id=user.id, team_id=team.id)

    def remove_member(self, membership):
        # also delete all subscriptions to team topics
        self._db.query(UserTeamTopic).filter(
            and_(
                UserTeamTopic.user_id == membership.user_id,
                TeamTopic.team_id == membership.team_id,
                UserTeamTopic.team_topic_id == TeamTopic.id,
            )
        ).delete(synchronize_session=False)

        self.delete(membership)

    def ensure_member(self, user_id: UUID, team_id: UUID) -> Optional[object]:
        """Ensure that user_id is member of team"""
        if not self.get_by_kwargs(user_id=user_id, team_id=team_id):
            return self.create_from_kwargs(user_id=user_id, team_id=team_id)
        return None
