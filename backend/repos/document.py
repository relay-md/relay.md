# -*- coding: utf-8 -*-
from ..models.document import Document as ORMDocument
from . import DatabaseAbstractRepository


class Document(DatabaseAbstractRepository):
    ORM_Model = ORMDocument
