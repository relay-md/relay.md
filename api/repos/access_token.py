from . import DatabaseAbstractRepository
from ..models.access_token import AccessToken as ORMAccessToken

class AccessToken(DatabaseAbstractRepository):
    ORM_Model = ORMAccessToken
