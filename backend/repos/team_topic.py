# -*- coding: utf-8 -*-
from sqlalchemy import select

from ..models.team import Team
from ..models.team_topic import TeamTopic
from ..models.topic import Topic
from ..repos.team import TeamRepo
from .base import DatabaseAbstractRepository


class TeamTopicRepo(DatabaseAbstractRepository):
    ORM_Model = TeamTopic

    def from_string(self, team_topic_str: str) -> TeamTopic:
        # import here due to cicular dependencies
        from ..exceptions import BadRequest, NotAllowed

        if "@" not in team_topic_str:
            raise BadRequest(f"topic@team format violated with {team_topic_str}")
        topic, team = team_topic_str.split("@")
        # TODO: maybe use repo here
        team_topic = self._db.scalar(
            select(TeamTopic)
            .join(Topic)
            .join(Team)
            .filter(Team.name == team.lower(), Topic.name == topic.lower())
        )
        if team_topic:
            return team_topic
        team_repo = TeamRepo(self._db)
        team = team_repo.get_by_kwargs(name=team)
        if not team:
            raise BadRequest(f"Team '{team}' does not exist!")
        # TODO: add an attribute to team so we can enable topic creation
        raise NotAllowed("Topic creation is not allowed yet")
