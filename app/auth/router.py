import uuid
from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.auth.schemas import UserCreate, UserRead, UserUpdate
from .models import User
from .service import get_user_manager, auth_backend


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
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
)



current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)