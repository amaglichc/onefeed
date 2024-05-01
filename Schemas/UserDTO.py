from enum import Enum

from pydantic import BaseModel, EmailStr

from Schemas.PostDTO import PostDTO


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"


class UserAddDTO(BaseModel):
    password: str
    username: str
    email: EmailStr
    role: RoleEnum
    posts: list[PostDTO] = []


class UserDTO(UserAddDTO):
    id: int
