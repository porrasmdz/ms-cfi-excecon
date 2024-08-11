
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from ..models import BaseSQLModel, Base
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
)

class User(SQLAlchemyBaseUserTableUUID, BaseSQLModel):
    pass

class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):  
    pass
    
class Role(BaseSQLModel):
    __tablename__ = "role"
    pass
class Permission(BaseSQLModel):
    __tablename__ = "permission"
    pass
#TODO: Define access control module/strategy or whatever I will be using


metadata = Base.metadata