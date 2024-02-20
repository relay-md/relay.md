# -*- coding: utf-8 -*-
from sqlalchemy import and_, exists, select

from ..models.team_topic import TeamTopic
from ..models.user import User
from .base import DatabaseAbstractRepository
from .team import Team
from .topic import Topic
from .user_team import UserTeamRepo
from .user_team_topic import UserTeamTopic, UserTeamTopicRepo


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
        if not user:
            return False
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

    def get_subscriptions(self, user: User, team: Team):
        return self._db.execute(
            select(
                TeamTopic,
                exists().where(
                    and_(
                        UserTeamTopic.team_topic_id == TeamTopic.id,
                        UserTeamTopic.user_id == user.id,
                    )
                ),
            ).filter(TeamTopic.team_id == team.id)
        )

    def has_subscribed_to_topic_in_team(
        self, user: User, team_topic: TeamTopic
    ) -> UserTeamTopic:
        return self._db.scalar(
            select(
                UserTeamTopic,
                exists().where(
                    and_(
                        UserTeamTopic.id == team_topic.id,
                        UserTeamTopic.user_id == user.id,
                    )
                ),
            )
        )
