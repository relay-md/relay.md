from . import DatabaseAbstractRepository
from ..models.document import Document as ORMDocument

class Document(DatabaseAbstractRepository):
    ORM_Model = ORMDocument
