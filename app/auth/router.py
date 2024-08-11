from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users import FastAPIUsers
from psycopg import IntegrityError
from app.auth import  schemas, service, utils
from app.auth.schemas import UserCreate, UserRead, UserUpdate
from app.dependencies import get_table_query_body
from app.schemas import PaginatedResource, TableQueryBody
from app.utils import filters_to_sqlalchemy
from .models import Permission, Role, User
from .service import get_user_manager, auth_backend
from app.database import get_session
from pydantic.type_adapter import TypeAdapter
from sqlalchemy.orm import Session 


router = APIRouter(tags=["Auth Module"])

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
router.include_router(fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    
)
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

@router.post("/roles/{role_id}/user/{user_id}", response_model=schemas.UserRead)
def assign_role(role_id: uuid.UUID, user_id: uuid.UUID, session: Session = Depends(get_session)):
    rbac= utils.RBACUtilities(session)
    role = rbac.get_single_registry(Role, role_id)
    user = rbac.get_single_registry(User, user_id)
    rbac.assign_user_to_role(user, role)
    return user

@router.post("/permission/{permission}/user/{user_id}", response_model=schemas.UserRead)
def assign_permission(permission: uuid.UUID, user_id: uuid.UUID, session: Session = Depends(get_session)):
    rbac= utils.RBACUtilities(session)
    permission = rbac.get_single_registry(Permission, permission)
    user = rbac.get_single_registry(User, user_id)
    rbac.assign_permission_to_user(user=user,permission=permission)
    return user
    
@router.post("/permission/{permission}/role/{role_id}", response_model=schemas.RoleRead)
def assign_permission_to_role(permission: uuid.UUID, role_id: uuid.UUID, session: Session = Depends(get_session)):
    try:
        rbac= utils.RBACUtilities(session)
        permission = rbac.get_single_registry(Permission, permission)
        role = rbac.get_single_registry(Role, role_id)
        rbac.assign_permission_to_role(role=role,permission=permission)
        return role
    except IntegrityError as ie:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ie))
    except Exception as e:
        raise e



@router.get("/permissions/", response_model=PaginatedResource[schemas.PermissionRead])
def read_permissions(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    rbac= utils.RBACUtilities(session)
    filters = filters_to_sqlalchemy(model=Permission, filters=tqb.filters) 
    (total_ccounts, cyclic_counts)= rbac.read_all_registries(model=Permission, filters=filters, 
                                                    tqb=tqb)
    response = PaginatedResource(totalResults=total_ccounts, results=cyclic_counts, 
                                skip= tqb.skip, limit=tqb.limit)
    return response
@router.get("/roles/", response_model=PaginatedResource[schemas.RoleRead])
def read_roles(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    rbac= utils.RBACUtilities(session)
    filters = filters_to_sqlalchemy(model=Role, filters=tqb.filters) 
    (total_ccounts, cyclic_counts)= rbac.read_all_registries(model=Role, filters=filters, 
                                                       tqb=tqb)
    response = PaginatedResource(totalResults=total_ccounts, results=cyclic_counts, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response
    
@router.post("/permissions/", response_model=schemas.PermissionRead)
def create_permission(permission: schemas.PermissionCreate, session: Session = Depends(get_session)):
    rbac = utils.RBACUtilities(session=session)
    result_perms = rbac.create_permission(permission=permission) 
    
    return schemas.PermissionRead.model_validate(result_perms[0])

@router.post("/roles/", response_model=schemas.RoleRead)
def create_role(role: schemas.RoleCreate, session: Session = Depends(get_session)):
    rbac = utils.RBACUtilities(session=session)
    role = rbac.create_role(role=role) 
    return schemas.RoleRead.model_validate(role)
