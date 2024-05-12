from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from Auth.Security import check_user_access, get_token_payload, get_user_by_payload, check_user_admin
from Schemas.PostDTO import PostDTO, PostAddDTO
from Schemas.UserDTO import UserDTO, UserAddDTO
from repos import UserRepo, PostRepo

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
count = 0


@router.get("", response_model=list[UserDTO])
async def get_users(token_payload: Annotated[dict, Depends(get_token_payload)]) -> list[UserDTO]:
    if check_user_admin(await get_user_by_payload(token_payload)):
        res = await UserRepo.get_all_users()
        return res
    raise HTTPException(status_code=403, detail="Access Denied")


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, token_payload: Annotated[dict, Depends(get_token_payload)]) -> UserDTO:
    if await check_user_access(user_id, token_payload):
        res = await UserRepo.get_user_by_id(user_id)
        return res


@router.get("/{user_id}/posts", response_model=list[PostDTO])
async def get_user_posts(user_id: int) -> list[PostDTO]:
    res = await PostRepo.get_post_by_user_id(user_id)
    return res


# @router.post("", response_model=UserDTO)
# def create_user(user: UserAddDTO) -> UserDTO:
#     return UserRepo.create_user(user)


@router.post("/posts", response_model=PostDTO)
async def create_user_posts(post: PostAddDTO,
                            token_payload: Annotated[dict, Depends(get_token_payload)]) -> PostDTO:
    res = await PostRepo.create_post(token_payload["id"], post)
    return res


@router.put("/{user_id}", response_model=UserDTO)
async def update_user(user_id: int, user: UserAddDTO,
                      token_payload: Annotated[dict, Depends(get_token_payload)]) -> UserDTO:
    if await check_user_access(user_id, token_payload):
        res = await UserRepo.update_user(user_id, user)
        return res


@router.delete("/{user_id}")
async def delete_user(user_id: int, token_payload: Annotated[dict, Depends(get_token_payload)]) -> dict[str, str]:
    if await check_user_access(user_id, token_payload):
        await UserRepo.delete_user(user_id)
        return {"message": "user has been deleted"}
