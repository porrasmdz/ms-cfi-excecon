
import uuid
from typing import Optional
from fastapi_users.authentication import BearerTransport
from fastapi_users import UUIDIDMixin, BaseUserManager
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from app.config import settings
from app.service import DatabaseRepository
from .dependencies import get_database_strategy, get_user_db
from .models import Permission, Role, User
from fastapi import Request, Depends

bearer_transport = BearerTransport(tokenUrl="auth/login")

SECRET = settings.DB_SECRET


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"Verification requested for user {user.id}. Verification token: {token}")
    # OVERRIDE OTHER METHODS https://fastapi-users.github.io/fastapi-users/latest/configuration/user-manager/


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name="database",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

role_crud = DatabaseRepository(model=Role)
permission_crud = DatabaseRepository(model=Permission)