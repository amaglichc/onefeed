from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select, delete

import Auth.SecurityUtils as authUtils
from Schemas.UserDTO import UserDTO, UserAddDTO
from database.core import sessionmaker
from orms.UserOrm import UserOrm


def get_all_users() -> list[UserDTO]:
    with sessionmaker() as session:
        return [UserDTO.model_validate(row, from_attributes=True) for row in
                session.execute(select(UserOrm)).scalars().all()]


def get_user_by_id(user_id: int) -> UserDTO:
    with sessionmaker() as session:
        user: UserOrm = session.get(UserOrm, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"User with id {user_id} not found"
                }
            )
        return UserDTO.model_validate(user, from_attributes=True)


def get_user_by_email(email: EmailStr) -> UserDTO:
    with sessionmaker() as session:
        user: UserOrm = session.execute(select(UserOrm).where(UserOrm.email == email))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"User with email {email} not found"
                }
            )
        convert_user = user.scalar()
    return UserDTO.model_validate(convert_user, from_attributes=True)


def create_user(user: UserAddDTO) -> UserDTO:
    with sessionmaker() as session:
        user.password = authUtils.hash_password(user.password).decode("utf8")
        user_orm: UserOrm = UserOrm(**user.model_dump())
        session.add(user_orm)
        session.flush()
        session.commit()
        return UserDTO.model_validate(user_orm, from_attributes=True)


def update_user(user_id: int, user: UserAddDTO) -> UserDTO:
    with sessionmaker() as session:
        user_orm: UserOrm = session.get(UserOrm, user_id)
        if user_orm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"User with id {user_id} not found"
                }
            )
        user_orm.username = user.username
        user_orm.email = user.email
        user_orm.role = user.role
        user_orm.posts = user.posts
        user_orm.isActive = user.isActive
        session.commit()
        return UserDTO.model_validate(user_orm, from_attributes=True)


def delete_user(user_id: int) -> None:
    with sessionmaker() as session:
        session.execute(delete(UserOrm).where(UserOrm.id == user_id))
        session.commit()
