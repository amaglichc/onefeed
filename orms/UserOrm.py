from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Schemas.UserDTO import RoleEnum
from database.core import Base

if TYPE_CHECKING:
    from orms.PostOrm import PostOrm


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    role: Mapped[RoleEnum] = mapped_column(nullable=False, server_default=RoleEnum.user, default=RoleEnum.user)
    isActive: Mapped[bool] = mapped_column(nullable=False, default=True, server_default="True")
    posts: Mapped[list["PostOrm"]] = relationship(
        back_populates="creator",
        lazy="selectin",
        cascade="all, delete,delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc',now())"))
