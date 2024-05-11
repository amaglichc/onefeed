from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from Auth.Security import check_user_access, get_token_payload
from Schemas.PostDTO import PostDTO, PostAddDTO
from Schemas.UserDTO import UserDTO, UserAddDTO, RoleEnum
from repos import UserRepo, PostRepo

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
count = 0


@router.get("", response_model=list[UserDTO])
def get_users(token_payload: Annotated[dict, Depends(get_token_payload)]) -> list[UserDTO]:
    if token_payload["role"] == RoleEnum.admin:
        return UserRepo.get_all_users()
    raise HTTPException(status_code=403, detail="Access Denied")


@router.get("/{user_id}", response_model=UserDTO)
def get_user(user_id: int, token_payload: Annotated[dict, Depends(get_token_payload)]) -> UserDTO:
    if check_user_access(user_id, token_payload):
        return UserRepo.get_user_by_id(user_id)


@router.get("/{user_id}/posts", response_model=list[PostDTO])
def get_user_posts(user_id: int) -> list[PostDTO]:
    return PostRepo.get_post_by_user_id(user_id)


# @router.post("", response_model=UserDTO)
# def create_user(user: UserAddDTO) -> UserDTO:
#     return UserRepo.create_user(user)


@router.post("/posts", response_model=PostDTO)
def create_user_posts(post: PostAddDTO,
                      token_payload: Annotated[dict, Depends(get_token_payload)]) -> PostDTO:
    return PostRepo.create_post(token_payload["id"], post)


@router.put("/{user_id}", response_model=UserDTO)
def update_user(user_id: int, user: UserAddDTO, token_payload: Annotated[dict, Depends(get_token_payload)]) -> UserDTO:
    if check_user_access(user_id, token_payload):
        return UserRepo.update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: int, token_payload: Annotated[dict, Depends(get_token_payload)]) -> dict[str, str]:
    if check_user_access(user_id, token_payload):
        UserRepo.delete_user(user_id)
        return {"message": "user has been deleted"}


@router.get("test")
def test():
    global count
