from fastapi import APIRouter

from Schemas.PostDTO import PostDTO, PostAddDTO
from Schemas.UserDTO import UserDTO, UserAddDTO
from repos import UserRepo, PostRepo

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("")
def get_users() -> list[UserDTO]:
    return UserRepo.get_all_users()


@router.get("/{user_id}")
def get_user(user_id: int) -> UserDTO:
    return UserRepo.get_user_by_id(user_id)


@router.get("/{user_id}/posts")
def get_user_posts(user_id: int) -> list[PostDTO]:
    return PostRepo.get_post_by_user_id(user_id)


@router.post("")
def create_user(user: UserAddDTO) -> UserDTO:
    return UserRepo.create_user(user)


@router.post("/{user_id}/posts")
def create_user_posts(user_id: int, post: PostAddDTO) -> PostDTO:
    return PostRepo.create_post(user_id, post)


@router.put("/{user_id}")
def update_user(user_id: int, user: UserAddDTO) -> UserDTO:
    return UserRepo.update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: int) -> dict[str, str]:
    UserRepo.delete_user(user_id)
    return {"message": "user has been deleted"}
