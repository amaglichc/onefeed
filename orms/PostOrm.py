from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base
from orms.CommentOrm import CommentOrm
from orms.UserOrm import UserOrm

if TYPE_CHECKING:
    from orms.UserOrm import UserOrm


class PostOrm(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    likes: Mapped[int] = mapped_column(default=0, server_default="0")
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    comments: Mapped[list["CommentOrm"]] = relationship(back_populates="post", lazy="selectin")
    creator: Mapped["UserOrm"] = relationship(
        back_populates="posts",
        lazy="selectin"
    )
