from typing import List, Literal, Optional, Set
import uuid
from fastapi_users import schemas
from app.schemas import ReadSchema, CreateSchema, UpdateSchema


################User Schemas
class UserRead(schemas.BaseUser[uuid.UUID], ReadSchema):
    roles: List["RoleRead"] = []
    permissions: List["PermissionRead"] = []


class UserCreate(schemas.BaseUserCreate, CreateSchema):
    pass


class UserUpdate(schemas.BaseUserUpdate, UpdateSchema):
    roles: Optional[List["RoleRead"]] = None
    permissions: Optional[List["PermissionRead"]] = None

##############Permission Schemas
class PermissionRead(ReadSchema):
    resource: str
    method: Literal["read" , "create" , "update" , "delete"] | uuid.UUID
    

class PermissionCreate(CreateSchema):
    resource: str
    methods: Set[Literal["read" , "create" , "update" , "delete"] | uuid.UUID] 

class PermissionUpdate(UpdateSchema):
    resource: Optional[str] = None
    methods: Optional[Set[Literal["read",
                                  "create", 
                                  "update", 
                                  "delete"] | uuid.UUID]] = [] 
    

##############Role Schemas
class RoleRead(ReadSchema):
    name: str
    description: str 
    permissions: List["PermissionRead"] = []


class RoleCreate(CreateSchema):
    name: str
    description: Optional[str] = None 

class RoleUpdate(UpdateSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    
    permissions: Optional[List["PermissionRead"]] = None