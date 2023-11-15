# -*- coding: utf-8 -*-
from ..models.user import User
from . import DatabaseAbstractRepository


class UserRepo(DatabaseAbstractRepository):
    ORM_Model = User
