from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users import FastAPIUsers
from psycopg import IntegrityError
from app.auth import schemas, service, utils
from app.auth.schemas import UserCreate, UserRead, UserUpdate
from app.dependencies import get_table_query_body
from app.schemas import PaginatedResource, TableQueryBody
from app.service import ResourceRouter
from app.utils import filters_to_sqlalchemy
from .models import Permission, Role, User
from .service import get_user_manager, auth_backend
from app.database import get_session
from pydantic.type_adapter import TypeAdapter
from sqlalchemy.orm import Session


router = APIRouter(tags=["Auth Module"])


class PermissionRouter(ResourceRouter):
    def create(self):
        print("THIS METHOD IS CREATE BEING CALLED :D")
        @self.router.post("/permissions/", response_model=schemas.PermissionRead)
        def create_permission(permission: schemas.PermissionCreate, session: Session = Depends(get_session)):    
            rbac = utils.RBACUtilities(session=session)
            result_perms = rbac.create_permission(permission=permission)
            return schemas.PermissionRead.model_validate(result_perms[0])
    def get_new_crud_routes(self) -> APIRouter:
        self.get_all()
        self.get_one()
        self.create()
        self.update()
        self.delete()
        return self.router

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

role_router = ResourceRouter(model=Role, name="roles",
                             model_repo=service.role_crud,
                             read_schema=schemas.RoleRead,
                             detailed_schema=schemas.RoleRead,
                             create_schema=schemas.RoleCreate,
                             update_schema=schemas.RoleUpdate
                             )

permission_router = PermissionRouter(model= Permission, name="permissions",
                                   model_repo=service.permission_crud,
                                   read_schema=schemas.PermissionRead, detailed_schema=schemas.PermissionRead,
                                   create_schema=schemas.PermissionCreate, update_schema=schemas.PermissionUpdate
)


@router.post("/roles/{role_id}/user/{user_id}", response_model=schemas.UserRead)
def assign_role(role_id: uuid.UUID, user_id: uuid.UUID, session: Session = Depends(get_session)):
    rbac = utils.RBACUtilities(session)
    role = rbac.get_single_registry(Role, role_id)
    user = rbac.get_single_registry(User, user_id)
    rbac.assign_user_to_role(user, role)
    return user


@router.post("/permission/{permission}/user/{user_id}", response_model=schemas.UserRead)
def assign_permission(permission: uuid.UUID, user_id: uuid.UUID, session: Session = Depends(get_session)):
    rbac = utils.RBACUtilities(session)
    permission = rbac.get_single_registry(Permission, permission)
    user = rbac.get_single_registry(User, user_id)
    rbac.assign_permission_to_user(user=user, permission=permission)
    return user


@router.post("/permission/{permission}/role/{role_id}", response_model=schemas.RoleRead)
def assign_permission_to_role(permission: uuid.UUID, role_id: uuid.UUID, session: Session = Depends(get_session)):
    try:
        rbac = utils.RBACUtilities(session)
        permission = rbac.get_single_registry(Permission, permission)
        role = rbac.get_single_registry(Role, role_id)
        rbac.assign_permission_to_role(role=role, permission=permission)
        return role
    except IntegrityError as ie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ie))
    except Exception as e:
        raise e


router.include_router(role_router.get_crud_routes())
router.include_router(permission_router.get_crud_routes())
router.include_router(fastapi_users.get_auth_router(auth_backend),
                      prefix="/auth")
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",

)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",

)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",

)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)

