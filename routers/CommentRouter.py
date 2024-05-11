from typing import Annotated

from fastapi import APIRouter, Depends

from Auth.Security import get_user_by_payload, check_user_access, get_token_payload
from Schemas.CommentDTO import CommentAddDTO
from Schemas.PostDTO import PostDTO
from Schemas.UserDTO import UserDTO
from repos import CommentRepo, PostRepo

router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["comments"]
)


@router.get("/{comment_id}", response_model=PostDTO)
def give_like(post_id: int, comment_id: int) -> PostDTO:
    CommentRepo.increase_likes(comment_id)
    return PostRepo.get_post_by_id(post_id)


@router.post("", response_model=PostDTO)
def create_comment(post_id: int, comment: CommentAddDTO,
                   user: Annotated[UserDTO, Depends(get_user_by_payload)]) -> PostDTO:
    CommentRepo.create_comment(post_id=post_id, comment=comment, user_id=user.id)
    return PostRepo.get_post_by_id(post_id)


@router.put("/{comment_id}", response_model=PostDTO)
def update_comment(post_id: int, comment_id: int, comment: CommentAddDTO,
                   token_payload: dict = Depends(get_token_payload)) -> PostDTO:
    if check_user_access(user_id=CommentRepo.get_comment_by_id(comment_id).author_id, token_payload=token_payload):
        CommentRepo.update_comment(comment_id=comment_id, comment=comment)
        return PostRepo.get_post_by_id(post_id)


@router.delete("/{comment_id}", response_model=PostDTO)
def delete_comment(post_id: int, comment_id: int, token_payload: dict = Depends(get_token_payload)) -> PostDTO:
    if check_user_access(user_id=CommentRepo.get_comment_by_id(comment_id).author_id, token_payload=token_payload):
        CommentRepo.delete_comment(comment_id)
        return PostRepo.get_post_by_id(post_id)
