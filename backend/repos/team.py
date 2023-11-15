# -*- coding: utf-8 -*-
from ..models.team import Team
from . import DatabaseAbstractRepository


class TeamRepo(DatabaseAbstractRepository):
    ORM_Model = Team
