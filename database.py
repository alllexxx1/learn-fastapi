from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}

else:
    DATABASE_URL = (
        f'postgresql+asyncpg://'
        f'{settings.DB_USER}:{settings.DB_PASS}@'
        f'{settings.DB_HOST}:{settings.DB_PORT}/'
        f'{settings.DB_NAME}'
    )
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
