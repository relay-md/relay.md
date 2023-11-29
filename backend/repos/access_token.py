# -*- coding: utf-8 -*-
from ..models.access_token import AccessToken
from .base import DatabaseAbstractRepository


class AccessTokenRepo(DatabaseAbstractRepository):
    ORM_Model = AccessToken
