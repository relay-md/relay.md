# -*- coding: utf-8 -*-
from ..models.user_team_topic import UserTeamTopic
from .base import DatabaseAbstractRepository
from .team_topic import TeamTopicRepo
from .user_team import UserTeamRepo


class UserTeamTopicRepo(DatabaseAbstractRepository):
    ORM_Model = UserTeamTopic

    def create_from_kwargs(self, **kwargs):
        team_topic_repo = TeamTopicRepo(self._db)
        team_topic = team_topic_repo.get_by_id(kwargs["team_topic_id"])

        if not team_topic:
            raise ValueError("Invalid team_topic id!")

        # Let's make sure we are subscribed to the team when we subscribe to a
        # topic!
        # WARNING: This may raise. Then the user cannot subscribe to the topic!
        user_team_repo = UserTeamRepo(self._db)
        user_team_repo.ensure_member(
            user_id=kwargs["user_id"], team_id=team_topic.team_id
        )

        # Create subscription to topic here
        user_team_topic = super().create_from_kwargs(**kwargs)

        return user_team_topic
