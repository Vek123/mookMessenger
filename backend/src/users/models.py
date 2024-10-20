import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String, DateTime, func, JSON, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from database import Base

if TYPE_CHECKING:
    from messenger.models import Chat


class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    permissions: Mapped[JSON | None] = mapped_column(JSON())


class User(Base):
    __tablename__ = "user"
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
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped[Role] = relationship(Role)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __mapper_args__ = {"eager_defaults": True}
