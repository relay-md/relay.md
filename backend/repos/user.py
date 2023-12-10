# -*- coding: utf-8 -*-
from sqlalchemy import select

from ..config import get_config
from ..models.user import User
from .base import DatabaseAbstractRepository
from .team import Team
from .topic import Topic
from .user_team import UserTeamRepo
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

    def is_member(self, user: User, team: Team):
        user_team_topic_repo = UserTeamRepo(self._db)
        return user_team_topic_repo.get_by_kwargs(
            user_id=user.id,
            team_id=team.id,
        )

    def from_string(self, username):
        return self.get_by_kwargs(username=username)

    def search_username(self, name, limit=10):
        return self._db.scalars(
            select(User).filter(User.username.like(f"%{name}%")).limit(limit)
        )

    def create_from_kwargs(self, **kwargs):
        from ..exceptions import BadRequest, NotAllowed
        from ..repos.team_topic import TeamTopicRepo

        user = super().create_from_kwargs(**kwargs)

        # Automatically subscribe to some team topics
        team_topic_repo = TeamTopicRepo(self._db)
        user_team_topic_repo = UserTeamTopicRepo(self._db)
        for subscribe_to in get_config().NEW_USER_SUBSCRIBE_TO:
            try:
                team_topic = team_topic_repo.from_string(subscribe_to)
                user_team_topic_repo.create_from_kwargs(
                    user_id=user.id, team_topic_id=team_topic.id
                )
            except (BadRequest, NotAllowed):
                # may fail if the team topic does not exist
                # or creation of topic is not allowed
                pass
        return user
