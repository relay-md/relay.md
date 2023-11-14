# -*- coding: utf-8 -*-
from ..models.user import User as ORMUser
from . import DatabaseAbstractRepository


class User(DatabaseAbstractRepository):
    ORM_Model = ORMUser
