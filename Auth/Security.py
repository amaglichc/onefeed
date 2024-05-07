from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError

from Auth import SecurityUtils
from Schemas.UserDTO import RoleEnum
from repos import UserRepo, PostRepo

bearer = HTTPBearer()


def get_current_user(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]) -> dict:
    try:
        payload: dict = SecurityUtils.decode_jwt(token=cred.credentials)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )
    return payload


def check_user(user_id: int, token_payload: dict) -> bool:
    if (token_payload["id"] == user_id and UserRepo.get_user_by_id(user_id).isActive) or UserRepo.get_user_by_id(
            token_payload["id"]).role == RoleEnum.admin:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access Denied"
    )


def check_post_access(post_id: int, token_payload: dict) -> bool:
    if token_payload["id"] == PostRepo.get_post_by_id(post_id).creator_id and UserRepo.get_user_by_id(
            token_payload["id"]).isActive or UserRepo.get_user_by_id(
        token_payload["id"]).role == RoleEnum.admin:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access Denied"
    )
