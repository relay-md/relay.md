# -*- coding: utf-8 -*-
from ..models.topic import Topic
from .base import DatabaseAbstractRepository


class TopicRepo(DatabaseAbstractRepository):
    ORM_Model = Topic
