from sqlalchemy import select, delete

from Schemas.UserDTO import UserDTO, UserAddDTO
from database.core import sessionmaker
from orms.UserOrm import UserOrm


def get_all_users() -> list[UserDTO]:
    with sessionmaker() as session:
        return [UserDTO.model_validate(row, from_attributes=True) for row in
                session.execute(select(UserOrm)).scalars().all()]


def get_user_by_id(user_id: int) -> UserDTO:
    with sessionmaker() as session:
        return UserDTO.model_validate(session.get(UserOrm, user_id), from_attributes=True)


def create_user(user: UserAddDTO) -> UserDTO:
    with sessionmaker() as session:
        user_orm: UserOrm = UserOrm(**user.model_dump())
        session.add(user_orm)
        session.flush()
        session.commit()
        return UserDTO.model_validate(user_orm, from_attributes=True)


def update_user(user_id: int, user: UserAddDTO) -> UserDTO:
    with sessionmaker() as session:
        user_orm: UserOrm = session.get(UserOrm, user_id)
        user_orm.username = user.username
        user_orm.email = user.email
        user_orm.role = user.role
        user_orm.posts = user.posts
        session.commit()
        return UserDTO.model_validate(user_orm, from_attributes=True)


def delete_user(user_id: int) -> None:
    with sessionmaker() as session:
        session.execute(delete(UserOrm).where(UserOrm.id == user_id))
        session.commit()
