from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession, create_async_engine
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.DB_URL
ASYNC_SQLALCHEMY_DATABASE_URL = settings.ASYNC_DB_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL
)

#Was sessionmaker
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) #engine)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


Base = declarative_base()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

async def async_init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def init_db():
    Base.metadata.create_all(bind=engine)#engine)

