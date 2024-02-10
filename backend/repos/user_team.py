# -*- coding: utf-8 -*-
from uuid import UUID

from sqlalchemy import and_

from ..models.team_topic import TeamTopic
from ..models.user_team import UserTeam
from ..models.user_team_topic import UserTeamTopic
from .base import DatabaseAbstractRepository


class UserTeamRepo(DatabaseAbstractRepository):
    ORM_Model = UserTeam

    def add_member(self, user_id: UUID, team_id: UUID):
        self.create_from_kwargs(user_id=user_id, team_id=team_id)

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
