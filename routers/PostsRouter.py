from typing import Annotated

from fastapi import APIRouter, Depends

from Auth.Security import check_post_access, get_token_payload, check_user_active
from Schemas.PostDTO import PostAddDTO
from Schemas.PostDTO import PostDTO
from Schemas.UserDTO import UserDTO
from repos import PostRepo

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("", response_model=list[PostDTO])
def get_posts() -> list[PostDTO]:
    return PostRepo.get_all_posts()


@router.get("/{post_id}", response_model=PostDTO)
def get_post(post_id: int) -> PostDTO:
    return PostRepo.get_post_by_id(post_id)


@router.put("/{post_id}", response_model=PostDTO)
def update_post(post_id: int, post: PostAddDTO, token_payload: dict = Depends(get_token_payload)) -> PostDTO:
    if check_post_access(post_id, token_payload=token_payload):
        return PostRepo.update_post(post_id, post)


@router.delete("/{post_id}")
def delete_post(post_id: int, token_payload: dict = Depends(get_token_payload)) -> dict[str, str]:
    if check_post_access(post_id, token_payload=token_payload):
        PostRepo.delete_post(post_id)
        return {"message": "post has been deleted"}


@router.get("/{post_id}/likes")
def give_like(post_id: int, user_is_active: Annotated[UserDTO, Depends(check_user_active)]):
    return PostRepo.increase_likes(post_id)
