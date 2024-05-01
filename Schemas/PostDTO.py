from pydantic import BaseModel


class PostAddDTO(BaseModel):
    title: str
    content: str | None


class PostDTO(PostAddDTO):
    id: int
    creator_id: int
