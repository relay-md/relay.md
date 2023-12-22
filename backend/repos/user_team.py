# -*- coding: utf-8 -*-
from uuid import UUID

from ..models.user_team import UserTeam
from .base import DatabaseAbstractRepository


class UserTeamRepo(DatabaseAbstractRepository):
    ORM_Model = UserTeam

    def add_member(self, user_id: UUID, team_id: UUID):
        self.create_from_kwargs(user_id=user_id, team_id=team_id)

    def remove_member(self, membership):
        self.delete(membership)
