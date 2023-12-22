# -*- coding: utf-8 -*-
from sqlalchemy import func, select

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

    def team_name_search(self, team_name):
        return self._db.scalar(select(Team).filter_by(name=team_name))

    def list_with_count_members(self):
        member_count = func.count(UserTeam.team_id)
        return self._db.execute(
            select(Team, member_count)
            .outerjoin(UserTeam)
            .filter(Team.hide.is_(False))
            .group_by(Team.id)
            .order_by(member_count.desc())
        )
