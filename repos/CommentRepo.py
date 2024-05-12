from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from starlette import status

from Schemas.CommentDTO import CommentAddDTO, CommentDTO
from database.core import sessionmaker
from orms.CommentOrm import CommentOrm


async def get_comment_by_id(comment_id: int) -> CommentDTO:
    async with sessionmaker() as session:
        res: CommentOrm = await session.execute(
            select(CommentOrm).options(selectinload(CommentOrm.post)).where(CommentOrm.id == comment_id))
        comment = res.scalar()
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        return CommentDTO.model_validate(comment, from_attributes=True)


async def create_comment(comment: CommentAddDTO, post_id: int, user_id) -> CommentDTO:
    async with sessionmaker() as session:
        new_comment = CommentOrm(**comment.model_dump())
        new_comment.post_id = post_id
        new_comment.author_id = user_id
        session.add(new_comment)
        await session.commit()
        return CommentDTO.model_validate(new_comment, from_attributes=True)


async def increase_likes(comment_id: int) -> CommentDTO:
    async with sessionmaker() as session:
        res: CommentOrm = await session.execute(
            select(CommentOrm).options(selectinload(CommentOrm.post)).where(CommentOrm.id == comment_id))
        comment = res.scalar()
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        comment.likes += 1
        await session.flush()
        await session.commit()
        return CommentDTO.model_validate(comment, from_attributes=True)


async def update_comment(comment: CommentAddDTO, comment_id: int) -> CommentDTO:
    async with sessionmaker() as session:
        res: CommentOrm = await session.execute(
            select(CommentOrm).options(selectinload(CommentOrm.post)).where(CommentOrm.id == comment_id))
        old_comment = res.scalar()
        if old_comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        old_comment.body = comment.body
        await session.commit()
        await session.refresh(old_comment)
        return CommentDTO.model_validate(old_comment, from_attributes=True)


async def delete_comment(comment_id: int) -> None:
    async with sessionmaker() as session:
        await session.execute(delete(CommentOrm).where(CommentOrm.id == comment_id))
        await session.commit()
