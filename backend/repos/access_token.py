# -*- coding: utf-8 -*-
from ..models.access_token import AccessToken as ORMAccessToken
from . import DatabaseAbstractRepository


class AccessToken(DatabaseAbstractRepository):
    ORM_Model = ORMAccessToken
