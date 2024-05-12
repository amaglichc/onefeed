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
async def give_like(post_id: int, comment_id: int) -> PostDTO:
    await CommentRepo.increase_likes(comment_id)
    res = await PostRepo.get_post_by_id(post_id)
    return res


@router.post("", response_model=PostDTO)
async def create_comment(post_id: int, comment: CommentAddDTO,
                         user: Annotated[UserDTO, Depends(get_user_by_payload)]) -> PostDTO:
    await CommentRepo.create_comment(post_id=post_id, comment=comment, user_id=user.id)
    res = await PostRepo.get_post_by_id(post_id)
    return res


@router.put("/{comment_id}", response_model=PostDTO)
async def update_comment(post_id: int, comment_id: int, comment: CommentAddDTO,
                         token_payload: dict = Depends(get_token_payload)) -> PostDTO:
    comment = await CommentRepo.get_comment_by_id(comment_id)
    if check_user_access(user_id=comment.author_id, token_payload=token_payload):
        await CommentRepo.update_comment(comment_id=comment_id, comment=comment)
        res = await PostRepo.get_post_by_id(post_id)
        return res


@router.delete("/{comment_id}", response_model=PostDTO)
async def delete_comment(post_id: int, comment_id: int, token_payload: dict = Depends(get_token_payload)) -> PostDTO:
    comment = await CommentRepo.get_comment_by_id(comment_id)
    if check_user_access(user_id=comment.author_id, token_payload=token_payload):
        await CommentRepo.delete_comment(comment_id)
        res = await PostRepo.get_post_by_id(post_id)
        return res
