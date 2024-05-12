from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import Auth.SecurityUtils as authUtils
from Auth import SecurityUtils
from Schemas.UserDTO import RoleEnum, UserDTO
from repos import UserRepo, PostRepo

bearer = HTTPBearer()


def check_token_type(payload: dict, token_type: str) -> bool:
    if payload.get("type") == token_type:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )


def get_token_payload(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]) -> dict:
    try:
        payload: dict = SecurityUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )
    return payload


async def get_user_by_payload(payload: Annotated[dict, Depends(get_token_payload)]) -> UserDTO:
    res = await UserRepo.get_user_by_id(payload.get("id"))
    return res


def check_user_active(user: Annotated[UserDTO, Depends(get_user_by_payload)]):
    if user.isActive:
        return user.isActive
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive"
        )


def check_user_admin(user: Annotated[UserDTO, Depends(get_user_by_payload)]):
    if user.role == RoleEnum.admin:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


async def check_user_access(user_id: int, token_payload: dict) -> bool:
    user = await get_user_by_payload(token_payload)
    if token_payload["id"] == user_id and check_user_active(user) and check_token_type(
            token_payload, token_type="access") or check_user_admin(user):
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access Denied"
    )


async def check_post_access(post_id: int, token_payload: dict) -> bool:
    post = await PostRepo.get_post_by_id(post_id)
    user = await UserRepo.get_user_by_id(token_payload["id"])
    if token_payload["id"] == post.creator_id and user.isActive and check_token_type(
            token_payload, token_type="access") or token_payload["role"] == RoleEnum.admin:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access Denied"
    )


def create_access_token(user: UserDTO) -> str:
    payload = {
        "type": "access",
        "id": user.id,
        "email": user.email,
        "role": user.role
    }
    return authUtils.encode_jwt(payload=payload, expire_minutes=100)


def create_refresh_token(user: UserDTO) -> str:
    payload = {
        "type": "refresh",
        "id": user.id
    }
    return authUtils.encode_jwt(payload=payload, expire_minutes=60 * 24 * 30)
