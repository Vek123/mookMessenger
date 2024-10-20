from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Integer,
    ForeignKey,
    Table,
    Column,
)

from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


if TYPE_CHECKING:
    from users.models import User

chat_user = Table(
    "chat_user",
    Base.metadata,
    Column("chat_id", Integer(), ForeignKey("chat.id")),
    Column("user_id", Integer(), ForeignKey("user.id")),
)


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    sender: Mapped["User"] = relationship(backref="messages")
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    chat: Mapped["Chat"] = relationship(backref="messages")
    content: Mapped[str] = mapped_column(nullable=False)


class Chat(Base):
    __tablename__ = "chat"
    id: Mapped[int] = mapped_column(primary_key=True)
    members: Mapped[List["User"]] = relationship(
        secondary=chat_user, backref="chats"
    )
