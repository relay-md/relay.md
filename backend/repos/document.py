# -*- coding: utf-8 -*-
from ..models.document import Document
from . import DatabaseAbstractRepository


class DocumentRepo(DatabaseAbstractRepository):
    ORM_Model = Document


class DocumentBodyRepo(DatabaseAbstractRepository):
    # TODO: access to s3 documents
    # filename == document id
    # nested folder structure with 6 nested nibbles
    # maybe take a look at how sccache does it
    ORM_Model = Document
