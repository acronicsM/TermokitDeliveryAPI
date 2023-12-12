from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from deliveryapi.core.models import db_helper
from ..core.config import settings
from ..admin.users.crud import get_user_by_name
from ..core.models.users import User
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def authenticate_user(username: str, password: str, session: AsyncSession):
    unauthenticated = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user: User | None = await get_user_by_name(name=username, session=session)

    if user is None or not user.is_active or not user.verify_password(password):
        raise unauthenticated

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + settings.auth.access_token_expires_delta, "iat": datetime.utcnow()})

    encoded_jwt = jwt.encode(to_encode, key=settings.auth.SECRET_KEY, algorithm=settings.auth.algorithm)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user: User | None = await get_user_by_name(name=token_data.username, session=session)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    return current_user
