# -*- coding: utf-8 -*-
from ..models.team_member import TeamMember
from .base import DatabaseAbstractRepository


class TeamTopicRepo(DatabaseAbstractRepository):
    ORM_Model = TeamMember
