from fastapi import HTTPException
from sqlalchemy import delete
from starlette import status

from Schemas.CommentDTO import CommentAddDTO, CommentDTO
from database.core import sessionmaker
from orms.CommentOrm import CommentOrm


def get_comment_by_id(comment_id: int) -> CommentDTO:
    with sessionmaker() as session:
        comment: CommentOrm = session.get(CommentOrm, comment_id)
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        return CommentDTO.model_validate(comment, from_attributes=True)


def create_comment(comment: CommentAddDTO, post_id: int, user_id) -> CommentDTO:
    with sessionmaker() as session:
        new_comment = CommentOrm(**comment.model_dump())
        new_comment.post_id = post_id
        new_comment.author_id = user_id
        session.add(new_comment)
        session.commit()
        return CommentDTO.model_validate(new_comment, from_attributes=True)


def increase_likes(comment_id: int) -> CommentDTO:
    with sessionmaker() as session:
        comment: CommentOrm = session.get(CommentOrm, comment_id)
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        comment.likes += 1
        session.commit()
        return CommentDTO.model_validate(comment, from_attributes=True)


def update_comment(comment: CommentAddDTO, comment_id: int) -> CommentDTO:
    with sessionmaker() as session:
        old_comment: CommentOrm = session.get(CommentOrm, comment_id)
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        old_comment.body = comment.body
        session.commit()
        return CommentDTO.model_validate(old_comment, from_attributes=True)


def delete_comment(comment_id: int) -> None:
    with sessionmaker() as session:
        session.execute(delete(CommentOrm).where(CommentOrm.id == comment_id))
        session.commit()
