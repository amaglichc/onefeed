from pydantic import BaseModel


class CommentAddDTO(BaseModel):
    body: str



class CommentDTO(CommentAddDTO):
    id: int
    author_id: int
    post_id: int
    likes: int