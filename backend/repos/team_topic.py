# -*- coding: utf-8 -*-
from sqlalchemy import select

from ..models.team import Team
from ..models.team_topic import TeamTopic
from ..models.topic import Topic
from ..repos.team import TeamRepo
from ..repos.topic import TopicRepo
from .base import DatabaseAbstractRepository


class TeamTopicRepo(DatabaseAbstractRepository):
    ORM_Model = TeamTopic

    def from_string(self, team_topic_str: str) -> TeamTopic:
        # import here due to cicular dependencies
        from ..exceptions import BadRequest, NotAllowed

        if "@" not in team_topic_str:
            raise BadRequest(f"topic@team format violated with {team_topic_str}")
        topic_name, team_name = team_topic_str.split("@")
        # TODO: maybe use repo here
        team_topic = self._db.scalar(
            select(TeamTopic)
            .join(Topic)
            .join(Team)
            .filter(Team.name == team_name.lower(), Topic.name == topic_name.lower())
        )
        if team_topic:
            return team_topic

        # From here on, we know that the team topic does not exist
        team_repo = TeamRepo(self._db)
        team = team_repo.get_by_kwargs(name=team_name)
        if not team:
            # Teams cannot be created this way!
            raise BadRequest(f"Team '{team_name}' does not exist!")
        if not team.allow_create_topics:
            raise NotAllowed("Topic creation is not allowed yet")

        topic_repo = TopicRepo(self._db)
        topic = topic_repo.get_by_kwargs(name=topic_name)
        if not topic:
            topic = Topic(name=topic_name)
            self._db.add(topic)
            self._db.commit()
            self._db.refresh(topic)
        new_team_topic = TeamTopic(team_id=team.id, topic_id=topic.id)
        self._db.add(new_team_topic)
        self._db.commit()
        self._db.refresh(new_team_topic)
        return new_team_topic
