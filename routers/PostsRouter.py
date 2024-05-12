from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi import APIRouter, Depends

from Auth.Security import check_post_access, check_user_active, get_token_payload
from Schemas.PostDTO import PostAddDTO
from Schemas.PostDTO import PostDTO
from Schemas.UserDTO import UserDTO
from repos import PostRepo

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("", response_model=list[PostDTO])
async def get_posts() -> list[PostDTO]:
    res = await PostRepo.get_all_posts()
    return res


@router.get("/{post_id}", response_model=PostDTO)
async def get_post(post_id: int) -> PostDTO:
    res = await PostRepo.get_post_by_id(post_id)
    return res


@router.put("/{post_id}", response_model=PostDTO)
async def update_post(post_id: int, post: PostAddDTO,token_payload: Annotated[dict,Depends(get_token_payload)]) -> PostDTO:
    if await check_post_access(post_id,token_payload):
        res = await PostRepo.update_post(post_id, post)
        return res


@router.delete("/{post_id}")
async def delete_post(post_id: int,token_payload: Annotated[dict,Depends(get_token_payload)]) -> dict[str, str]:
    if await check_post_access(post_id,token_payload):
        await PostRepo.delete_post(post_id)
        return {"message": "post has been deleted"}


@router.get("/{post_id}/likes")
async def give_like(post_id: int, user_is_active: UserDTO = Depends(check_user_active)):
    if user_is_active:
        res = await PostRepo.increase_likes(post_id)
        return res
