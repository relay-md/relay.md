# -*- coding: utf-8 -*-
from ..models.document_access import DocumentAccess
from .base import DatabaseAbstractRepository


class DocumentAccessRepo(DatabaseAbstractRepository):
    ORM_Model = DocumentAccess
