import secrets
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper

# from .schemas import UserSchema, TokenSchema
from .schemas import TokenSchema

from .utils import authenticate_user, create_access_token

# from .utils import hash_password, encode_jwt, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBasic()

# admin = UserSchema(
#     username="admin",
#     password=hash_password("admin"),
# )
#
#
# user_db: dict[str, UserSchema] = {
#     admin.username: admin,
# }
#
#
# def auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
#     unauthenticated = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid username or password or user not activate",
#         headers={"WWW-Authenticate": "Basic"},
#     )
#
#     if not (user := user_db.get(credentials.username)):
#         raise unauthenticated
#
#     if not user.is_active:
#         raise unauthenticated
#
#     if not verify_password(password=credentials.password, hashed_password=user.password):
#         raise unauthenticated
#
#     return user


# @router.post(
#     path="/basic",
#     description="Базовая авторизация для получения JWT токена",
#     name="Авторизация",
# )
# async def basic_auth(user: UserSchema = Depends(auth_user_username)):
#     # return f"hi {auth_username}"
#     jwt_payload = {
#         "sub": user.username,
#         "username": user.username,
#     }
#     access_token = encode_jwt(jwt_payload)
#
#     return TokenSchema(token=access_token, token_type="Bearer")


# @router.post("login")
# async def login(user: UserSchema = Depends(auth_user_username)):
#     jwt_payload = {
#         "sub": user.username,
#         "username": user.username,
#     }
#     access_token = encode_jwt()
#
#     return TokenSchema(token=access_token, token_type="Bearer")


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    user = await authenticate_user(form_data.username, form_data.password, session=session)

    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
