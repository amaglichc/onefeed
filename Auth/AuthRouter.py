from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status, Query, Depends
from pydantic import EmailStr

import Auth.SecurityUtils as authUtils
from Auth.Security import create_access_token, create_refresh_token, get_user_by_payload, check_token_type, \
    get_token_payload
from Schemas.UserDTO import UserAddDTO, RoleEnum, UserDTO
from repos import UserRepo

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signup")
async def sign_up(email: Annotated[EmailStr, Form()],
                  password: Annotated[str, Query(min_length=10, max_length=50), Form()],
                  username: Annotated[str, Form()]):
    new_user: UserAddDTO = UserAddDTO(username=username, email=email, password=password, role=RoleEnum.user,
                                      isActive=True)
    await UserRepo.create_user(new_user)
    return {
        "message": "You have successfully registered",
        "status": status.HTTP_201_CREATED
    }


@router.post("/signin")
async def sign_in(email: Annotated[EmailStr, Form()], password: Annotated[str, Form()]):
    user: UserDTO = await UserRepo.get_user_by_email(email)
    if authUtils.validate_password(password, user.password.encode()):
        return {
            "access_token": create_access_token(user),
            "refresh_token": create_refresh_token(user),
            "token_type": "Bearer"
        }
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/refresh_token")
def refresh_token(payload: Annotated[dict, Depends(get_token_payload)],
                  user: Annotated[UserDTO, Depends(get_user_by_payload)]):
    if check_token_type(payload, "refresh"):
        token = create_access_token(user)
        return {"access_token": token,
                "token_type": "Bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
