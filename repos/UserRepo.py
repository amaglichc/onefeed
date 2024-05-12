from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

import Auth.SecurityUtils as authUtils
from Schemas.UserDTO import UserDTO, UserAddDTO
from database.core import sessionmaker
from orms.UserOrm import UserOrm


async def get_all_users() -> list[UserDTO]:
    async with sessionmaker() as session:
        res = await session.execute(select(UserOrm))
        users = res.scalars().all()
        return [UserDTO.model_validate(row, from_attributes=True) for row in
                users]


async def get_user_by_id(user_id: int) -> UserDTO:
    async with sessionmaker() as session:
        res: UserOrm = await session.execute(
            select(UserOrm).options(selectinload(UserOrm.posts)).where(UserOrm.id == user_id))
        user = res.scalar()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"User with id {user_id} not found"
                }
            )
        return UserDTO.model_validate(user, from_attributes=True)


async def get_user_by_email(email: EmailStr) -> UserDTO:
    async with sessionmaker() as session:
        res: UserOrm = await session.execute(
            select(UserOrm).options(selectinload(UserOrm.posts)).where(UserOrm.email == email))
        user = res.scalar()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": f"User with email {email} not found"
                }
            )
    return UserDTO.model_validate(user, from_attributes=True)


async def create_user(user: UserAddDTO) -> UserDTO:
    async with sessionmaker() as session:
        user.password = authUtils.hash_password(user.password).decode("utf8")
        user_orm: UserOrm = UserOrm(**user.model_dump())
        session.add(user_orm)
        await session.commit()
        return UserDTO.model_validate(user_orm, from_attributes=True)


async def update_user(user_id: int, user: UserAddDTO) -> UserDTO:
    async with sessionmaker() as session:
        res: UserOrm = await session.execute(
            select(UserOrm).options(selectinload(UserOrm.posts)).where(UserOrm.id == user_id))
        user_orm = res.scalar()
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
        await session.commit()
        await session.refresh(user_orm)
        return UserDTO.model_validate(user_orm, from_attributes=True)


async def delete_user(user_id: int) -> None:
    async with sessionmaker() as session:
        await session.execute(delete(UserOrm).where(UserOrm.id == user_id))
        await session.commit()
