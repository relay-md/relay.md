# -*- coding: utf-8 -*-
from ..models.user_team import UserTeam
from .base import DatabaseAbstractRepository


class UserTeamRepo(DatabaseAbstractRepository):
    ORM_Model = UserTeam
