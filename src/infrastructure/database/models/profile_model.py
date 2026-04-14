from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Text, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from .user_model import UserModel


class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    bio: Mapped[str|None] = mapped_column(
        Text,
        nullable=True,
    )

    avatar_url: Mapped[str|None] = mapped_column(
        String(500),
        nullable=True,
    )

    phone: Mapped[str|None] = mapped_column(
        String(20),
        nullable=True,
    )

    address: Mapped[str|None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="profile", lazy="joined")

    def __repr__(self):
        return f"<ProfileModel(id={self.id}, user_id={self.user_id})>"
