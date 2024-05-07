from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status
from pydantic import EmailStr

import Auth.SecurityUtils as authUtils
from Schemas.UserDTO import UserAddDTO, RoleEnum, UserDTO
from repos import UserRepo

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signup")
def sign_up(email: Annotated[EmailStr, Form()], password: Annotated[str, Form()], username: Annotated[str, Form()]):
    new_user: UserAddDTO = UserAddDTO(username=username, email=email, password=password, role=RoleEnum.user,
                                      isActive=True)
    UserRepo.create_user(new_user)
    return {
        "message": "You have successfully registered",
        "status": status.HTTP_201_CREATED
    }


@router.post("/signin")
def sign_in(email: Annotated[EmailStr, Form()], password: Annotated[str, Form()]):
    user: UserDTO = UserRepo.get_user_by_email(email)
    if authUtils.validate_password(password, user.password.encode()):
        payload = {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
        token = authUtils.encode_jwt(payload=payload)
        return {
            "access_token": token,
            "token_type": "Bearer"
        }
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
