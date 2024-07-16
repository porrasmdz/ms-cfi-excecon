from sqlalchemy import Boolean, Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from uuid import UUID
from ..models import BaseSQLModel
from datetime import date

class User(BaseSQLModel):
    __tablename__ = "user"
    pass
class Role(BaseSQLModel):
    __tablename__ = "role"
    pass
class Permission(BaseSQLModel):
    __tablename__ = "permission"
    pass
#TODO: Define access control module/strategy or whatever I will be using