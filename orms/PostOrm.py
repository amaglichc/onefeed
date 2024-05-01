from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base
from orms.UserOrm import UserOrm

if TYPE_CHECKING:
    from orms.UserOrm import UserOrm


class PostOrm(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    creator: Mapped["UserOrm"] = relationship(
        back_populates="posts",
        lazy="selectin"
    )
