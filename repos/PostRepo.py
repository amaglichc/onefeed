from fastapi import HTTPException, status
from sqlalchemy import select, delete

from Schemas.PostDTO import PostDTO, PostAddDTO
from database.core import sessionmaker
from orms.PostOrm import PostOrm


def get_all_posts() -> list[PostDTO]:
    with sessionmaker() as session:
        return [PostDTO.model_validate(row, from_attributes=True) for row in
                session.execute(select(PostOrm)).scalars().all()]


def get_post_by_id(post_id: int) -> PostDTO:
    with sessionmaker() as session:
        post: PostOrm = session.get(PostOrm, post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"Post with id {post_id} not found"
                }
            )
        return PostDTO.model_validate(post, from_attributes=True)


def create_post(user_id: int, post: PostAddDTO) -> PostDTO:
    with sessionmaker() as session:
        post_orm: PostOrm = PostOrm(**post.model_dump())
        session.add(post_orm)
        post_orm.creator_id = user_id
        session.flush()
        session.commit()
        return PostDTO.model_validate(post_orm, from_attributes=True)


def get_post_by_user_id(user_id: int) -> list[PostDTO]:
    with sessionmaker() as session:
        res = session.execute(select(PostOrm).where(PostOrm.creator_id == user_id))

        return [PostDTO.model_validate(row, from_attributes=True) for row in
                res.scalars().all()]


def update_post(post_id: int, post: PostAddDTO) -> PostDTO:
    with sessionmaker() as session:
        post_orm: PostOrm = session.get(PostOrm, post_id)
        post_orm.title = post.title
        post_orm.content = post.content
        session.commit()
        return PostDTO.model_validate(post_orm, from_attributes=True)


def delete_post(post_id: int) -> None:
    with sessionmaker() as session:
        session.execute(delete(PostOrm).where(PostOrm.id == post_id))
        session.commit()
