# -*- coding: utf-8 -*-
from uuid import UUID

from ..models.user_team import UserTeam
from .base import DatabaseAbstractRepository
from .billing import SubscriptionRepo


class UserTeamRepo(DatabaseAbstractRepository):
    ORM_Model = UserTeam

    def add_member(self, user_id: UUID, team_id: UUID):
        subscription_repo = SubscriptionRepo(self._db)
        subscription = subscription_repo.get_latest_subscription_for_team_id(team_id)
        if subscription:
            subscription_repo.update_quantity(subscription, subscription.quantity + 1)
        self.create_from_kwargs(user_id=user_id, team_id=team_id)

    def remove_member(self, membership):
        subscription_repo = SubscriptionRepo(self._db)
        subscription = subscription_repo.get_latest_subscription_for_team_id(
            membership.team_id
        )
        if subscription:
            subscription_repo.update_quantity(subscription, subscription.quantity - 1)
        self.delete(membership)
