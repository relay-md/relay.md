# -*- coding: utf-8 -*-
from ..models.user_team_topic import UserTeamTopic
from .base import DatabaseAbstractRepository


class UserTeamTopicRepo(DatabaseAbstractRepository):
    ORM_Model = UserTeamTopic
