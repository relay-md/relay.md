# -*- coding: utf-8 -*-
from ..models.document import Document
from . import DatabaseAbstractRepository


class DocumentRepo(DatabaseAbstractRepository):
    ORM_Model = Document
