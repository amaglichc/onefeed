from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base

if TYPE_CHECKING:
    from orms.PostOrm import PostOrm


class CommentOrm(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str]
    likes: Mapped[int] = mapped_column(default=0, server_default="0")
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    post: Mapped["PostOrm"] = relationship(back_populates="comments", lazy="selectin")
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete='CASCADE'))
