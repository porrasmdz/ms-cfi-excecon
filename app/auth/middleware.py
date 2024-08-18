
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.auth.constants import EXCLUDED_PATHS
from app.auth.models import User
from app.auth.utils import has_permission, translate_method_to_action
from fastapi import Request
from .router import fastapi_users
from app.database import get_session

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

async def check_user_permissions(request: Request,
                                 user: User = Depends(current_user),
                                 session: Session = Depends(get_session)):
    request_method = str(request.method).upper()
    action = translate_method_to_action(request_method)
    resource = request.url.path[1:]
    if not resource in EXCLUDED_PATHS:
        if not has_permission(user, resource, action, session):
            raise HTTPException(
                status_code=403, detail="Forbidden")
        
        
