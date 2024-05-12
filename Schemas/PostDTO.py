from pydantic import BaseModel

from Schemas.CommentDTO import CommentDTO


class PostAddDTO(BaseModel):
    title: str
    content: str | None


class PostDTO(PostAddDTO):
    id: int
    creator_id: int
    comments: list[CommentDTO]
    likes: int
