import uuid

from fastapi_users import schemas
from app.schemas import ReadSchema, CreateSchema, UpdateSchema

class UserRead(schemas.BaseUser[uuid.UUID], ReadSchema):
    pass


class UserCreate(schemas.BaseUserCreate, CreateSchema):
    pass


class UserUpdate(schemas.BaseUserUpdate, UpdateSchema):
    pass