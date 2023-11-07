from . import DatabaseAbstractRepository
from ..models.user import User as ORMUser

class User(DatabaseAbstractRepository):
    ORM_Model = ORMUser
