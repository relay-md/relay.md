# -*- coding: utf-8 -*-
from sqlalchemy import func, select

from ..models.billing import Subscription
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

    def list_selected_teams(self):
        member_count = func.count(UserTeam.team_id)
        return self._db.execute(
            select(Team, member_count)
            .outerjoin(UserTeam)
            .filter(Team.hide.is_(False), Team.favorit.is_(True))
            .group_by(Team.id)
            .order_by(member_count.desc())
        )

    def update_seats(self, team: Team, subscription: Subscription, new_seats: int):
        from .billing import SubscriptionRepo

        subscription_repo = SubscriptionRepo(self._db)
        subscription_repo.update_quantity(subscription, new_seats)
        self.update(team, seats=new_seats)

    def search_with_count(self, name, limit=10):
        member_count = func.count(UserTeam.team_id)
        return self._db.execute(
            select(Team, member_count)
            .outerjoin(UserTeam)
            .filter(Team.name.like(f"%{name}%"), Team.hide.is_(False))
            .group_by(Team.id)
            .order_by(member_count.desc())
            .limit(limit)
        )
