from fastapi import APIRouter

from Schemas.PostDTO import PostAddDTO
from Schemas.PostDTO import PostDTO
from repos import PostRepo

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("")
def get_posts() -> list[PostDTO]:
    return PostRepo.get_all_posts()


@router.get("/{post_id}")
def get_post(post_id: int) -> PostDTO:
    return PostRepo.get_post_by_id(post_id)


@router.post("")
def create_post(post: PostAddDTO) -> PostDTO:
    return PostRepo.create_post(post)


@router.put("/{post_id}")
def update_post(post_id: int, post: PostAddDTO) -> PostDTO:
    return PostRepo.update_post(post_id, post)


@router.delete("/{post_id}")
def delete_post(post_id: int) -> dict[str, str]:
    PostRepo.delete_post(post_id)
    return {"message": "post has been deleted"}
