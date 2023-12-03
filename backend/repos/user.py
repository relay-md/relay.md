# -*- coding: utf-8 -*-
from ..models.user import User
from .base import DatabaseAbstractRepository
from .team import Team
from .topic import Topic
from .user_team_topic import UserTeamTopicRepo


class UserRepo(DatabaseAbstractRepository):
    ORM_Model = User

    def is_subscribed(self, user: User, team: Team, topic: Topic):
        from ..repos.team_topic import TeamTopicRepo

        team_topic_repo = TeamTopicRepo(self._db)
        team_topic = team_topic_repo.get_by_kwargs(team_id=team.id, topic_id=topic.id)
        if not team_topic:
            return False
        user_team_topic_repo = UserTeamTopicRepo(self._db)
        return user_team_topic_repo.get_by_kwargs(
            user_id=user.id,
            team_topic_id=team_topic.id,
        )
