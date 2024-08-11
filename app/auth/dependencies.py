from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase)
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from app.config import settings
from .models import AccessToken, User
from app.database import get_async_session as get_session
from sqlalchemy.orm import Session

SECRET = settings.DB_SECRET

async def get_user_db(session: Session = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_access_token_db(
    session: Session = Depends(get_session),
):  
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)

def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    db_strat= DatabaseStrategy(access_token_db, lifetime_seconds=3600)
    
    return db_strat

# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=SECRET, lifetime_seconds=3600)



