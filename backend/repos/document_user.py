# -*- coding: utf-8 -*-
from ..models.document_user import DocumentUser
from .base import DatabaseAbstractRepository


class DocumentUserRepo(DatabaseAbstractRepository):
    ORM_Model = DocumentUser
