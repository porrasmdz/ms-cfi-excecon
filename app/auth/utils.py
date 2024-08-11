from typing import Any, List
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.auth.schemas import PermissionCreate, RoleCreate
from app.models import BaseSQLModel
from app.schemas import TableQueryBody
from app.service import get_paginated_resource
from .dependencies import get_session
from .models import Role, User, Permission
from fastapi import Depends, HTTPException


def get_user_permissions(user: User, session: Session):
    try:
        uq = select(User).where(User.id == user.id)
        user_res = session.execute(uq)
        found_user = user_res.scalars().first()
        if found_user is None:
            return []
        print("MY USER ON THIS CLASS FROM ID", found_user.roles)
        user_roles = found_user.roles
        user_permissions = found_user.permissions
        permissions = []
        if user_roles is not None:
            for role in user_roles:
                if role.permissions is not None:
                    for rperm in role.permissions:
                        permissions.append(rperm)
        if user_permissions is not None:
            for permission in user_permissions:
                permissions.append(permission)
        return permissions
    except Exception as e:
        print("EXCEPTION OCURRED ", str(e))


class RBACUtilities():
    def __init__(self, session: Session):
        self.session = session

    def create_role(self, role: RoleCreate):
        new_role = Role(**role.model_dump())
        self.session.add(new_role)
        self.session.commit()
        self.session.refresh(new_role)
        
        return new_role

    def create_permission(self, permission: PermissionCreate):
        created_perms = []
        for method in permission.methods:
            new_permission = Permission(
                resource=permission.resource, 
                method=method, 
                created_at=permission.created_at, 
                updated_at=permission.updated_at,
                deleted_at=permission.deleted_at)
            created_perms.append(new_permission)
            self.session.add(new_permission)
            self.session.commit()
            self.session.refresh(new_permission)
        return created_perms

    def assign_permission_to_user(self, permission: Permission,
                                  user: User
                                  ):
        permission.users.append(user)
        self.session.commit()
        self.session.refresh(permission)

    def assign_permission_to_role(self, permission: Permission,
                                  role: Role
                                  ):
        permission.roles.append(role)
        self.session.commit()
        self.session.refresh(permission)

    def assign_user_to_role(self, user: User,
                            role: Role
                            ):
        
        user.roles.append(role)
        self.session.commit()
        self.session.refresh(user)

    def read_all_registries(self, model:BaseSQLModel, filters: List[Any], tqb: TableQueryBody):
        return get_paginated_resource(model, filters, tqb, self.session)
    def get_single_registry(self, model:BaseSQLModel, reg_id):
        result = self.session.query(model).filter(model.id == reg_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Registry not found")
        return result
# rbac = RBACUtilities()


def translate_method_to_action(method: str) -> str:
    method_permission_mapping = {
        "GET": "read",
        "POST": "create",
        "PUT": "update",
        "DELETE": "delete",
    }
    return method_permission_mapping.get(method.upper(), "read")

# CHeck if permission granted or not


def has_permission(user: User, resource_name: str, required_permission: str, session: Session):
    try:
        target_resource = resource_name.replace("/","")
        if user.is_superuser:
            return True
        user_permissions = get_user_permissions(user, session=session)
        print("USER PERMISSIONS OBTAINED", user_permissions)
        if user_permissions is None:
            return False
        filtered_permissions = filter(
            lambda up: up.resource == target_resource, user_permissions)
        
        for perm in filtered_permissions:
            if perm.method == required_permission:
                return True

        return False
    except Exception as e:
        print("OCURRIO UN ERROR AL OBTENER PERMISOS DE USUARIO", str(e))
        return False
