from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from ..models import BaseSQLModel, Base
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
)

role_permission_table = Table(
    "role_permission_table",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True)
)


user_permission_table = Table(
    "user_permission_table",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True)
)

user_role_table = Table(
    "user_role_table",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True)
)

class User(SQLAlchemyBaseUserTableUUID, BaseSQLModel):
    permissions: Mapped[Optional[List["Permission"]]] = relationship(
        secondary=user_permission_table,back_populates="users", lazy="selectin"
    )
    roles: Mapped[Optional[List["Role"]]] = relationship(
        secondary=user_role_table, back_populates="users", lazy="selectin"
    )

class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):  
    pass


#############RBAC Models
class Role(BaseSQLModel):
    __tablename__ = "role"
    name : Mapped[str] = mapped_column()
    description : Mapped[Optional[str]] = mapped_column()
    # backwards users relation
    # m2m to permissions DONE
    # m2m to users DONE
    users: Mapped[Optional[List["User"]]] = relationship(
        secondary=user_role_table, back_populates="roles"
    )
    
    permissions: Mapped[Optional[List["Permission"]]] = relationship(
        secondary=role_permission_table, back_populates="roles", lazy="selectin"
    )

class Permission(BaseSQLModel):
    __tablename__ = "permission"
    resource:  Mapped[str] = mapped_column()
    method:  Mapped[str] = mapped_column()
    # m2m users DONE
    # m2m roles DON
    users: Mapped[Optional[List["User"]]] = relationship(
        secondary=user_permission_table, back_populates="permissions"
    )
    
    roles: Mapped[Optional[List["Role"]]] = relationship(
        secondary=role_permission_table, back_populates="permissions"
    )
    
#TODO: Define access control module/strategy or whatever I will be using


metadata = Base.metadata