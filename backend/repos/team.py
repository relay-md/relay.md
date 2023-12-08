# -*- coding: utf-8 -*-
from sqlalchemy import select

from ..models.team import Team
from ..models.user_team import UserTeam
from .base import DatabaseAbstractRepository


class TeamRepo(DatabaseAbstractRepository):
    ORM_Model = Team

    def list_team_members(self, team: Team, page: int = 0, size: int = 10):
        return list(
            self._db.scalars(
                select(UserTeam)
                .filter(UserTeam.team_id == team.id)
                .offset(page * size)
                .limit(size)
            )
        )
