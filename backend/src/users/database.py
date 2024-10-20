import datetime
from typing import AsyncGenerator, List, TYPE_CHECKING

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy import String, TIMESTAMP, Boolean, ForeignKey, DateTime, func


from settings import DATABASE_CONFIG
from src.database import Base
from messenger.models import chat_user, Message, Chat
from users.models import Role, User as Usr


DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{DATABASE_CONFIG["DB_USER"]}"
    f":{DATABASE_CONFIG["DB_PASS"]}"
    f"@{DATABASE_CONFIG["DB_HOST"]}"
    f":{DATABASE_CONFIG["DB_PORT"]}"
    f"/{DATABASE_CONFIG["DB_NAME"]}"
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(), server_default=func.now(), nullable=True,
    )
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id))
    role: Mapped[Role] = relationship(Role, uselist=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __mapper_args__ = {"eager_defaults": True}


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
