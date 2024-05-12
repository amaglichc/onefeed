from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from Schemas.PostDTO import PostDTO, PostAddDTO
from database.core import sessionmaker
from orms.PostOrm import PostOrm


async def get_all_posts() -> list[PostDTO]:
    async with sessionmaker() as session:
        res = await session.execute(select(PostOrm))
        posts = res.scalars().all()
        return [PostDTO.model_validate(row, from_attributes=True) for row in posts]


async def get_post_by_id(post_id: int) -> PostDTO:
    async with sessionmaker() as session:
        res: PostOrm = await session.execute(
            select(PostOrm).options(selectinload(PostOrm.creator)).options(selectinload(PostOrm.comments)).where(
                PostOrm.id == post_id))
        post = res.scalar()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"Post with id {post_id} not found"
                }
            )
        return PostDTO.model_validate(post, from_attributes=True)


async def create_post(user_id: int, post: PostAddDTO) -> PostDTO:
    async with sessionmaker() as session:
        post_orm: PostOrm = PostOrm(**post.model_dump())
        post_orm.creator_id = user_id
        post_orm.comments = []
        session.add(post_orm)
        await session.commit()
        return PostDTO.model_validate(post_orm, from_attributes=True)


async def get_post_by_user_id(user_id: int) -> list[PostDTO]:
    async with sessionmaker() as session:
        res = await session.execute(
            select(PostOrm).options(selectinload(PostOrm.creator)).options(selectinload(PostOrm.comments)).where(
                PostOrm.creator_id == user_id))
        posts = res.scalars().all()
        if posts is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Posts not found"
                }
            )
        return [PostDTO.model_validate(row, from_attributes=True) for row in
                posts]


async def update_post(post_id: int, post: PostAddDTO) -> PostDTO:
    async with sessionmaker() as session:
        res: PostOrm = await session.execute(
            select(PostOrm).options(selectinload(PostOrm.creator)).options(selectinload(PostOrm.comments)).where(
                PostOrm.id == post_id))
        post_orm = res.scalar()
        if post_orm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"Post with id {post_id} not found"
                }
            )
        post_orm.title = post.title
        post_orm.content = post.content
        await session.commit()
        await session.refresh(post_orm)
        return PostDTO.model_validate(post_orm, from_attributes=True)


async def increase_likes(post_id: int) -> PostDTO:
    async with sessionmaker() as session:
        res: PostOrm = await session.execute(
            select(PostOrm).options(selectinload(PostOrm.creator)).options(selectinload(PostOrm.comments)).where(
                PostOrm.id == post_id))
        post_orm = res.scalar()
        if post_orm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"Post with id {post_id} not found"
                }
            )
        post_orm.likes += 1
        await session.flush()
        await session.commit()
        return PostDTO.model_validate(post_orm, from_attributes=True)


async def delete_post(post_id: int) -> None:
    async with sessionmaker() as session:
        await session.execute(delete(PostOrm).where(PostOrm.id == post_id))
        await session.commit()
