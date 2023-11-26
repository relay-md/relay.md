# -*- coding: utf-8 -*-
from ..models.user import User
from .base import DatabaseAbstractRepository


class UserRepo(DatabaseAbstractRepository):
    ORM_Model = User
