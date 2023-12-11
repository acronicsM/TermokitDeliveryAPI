import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBasic()

d = {
    "admin": "admin",
}


def auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    unauthenticated = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    if not (correct_password := d.get(credentials.username)):
        raise unauthenticated

    if not secrets.compare_digest(credentials.password.encode("utf-8"), correct_password.encode("utf-8")):
        raise unauthenticated

    return credentials.username


@router.get(
    path="/basic",
    description="Базовая авторизация для получения JWT токена",
    name="Авторизация",
)
async def basic_auth(auth_username: str = Depends(auth_user_username)):
    return f"hi {auth_username}"
