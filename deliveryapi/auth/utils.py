from datetime import timedelta, datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from ..core.config import settings
from ..admin.users.crud import get_user_by_name
from ..core.models.users import User

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#
# def encode_jwt(
#     payload: dict,
#     key: str = settings.auth.jwt_privet_key.read_text(),
#     algorithm: str = settings.auth.algorithm,
#     experi_timedelta: timedelta = settings.auth.access_token_expires_delta,
# ):
#     to_encode = payload.copy()
#     # to_encode.update(exp=datetime.utcnow() + experi_timedelta, iat=datetime.utcnow())
#
#     encoded = jwt.encode(payload=to_encode, key=key, algorithm=algorithm)
#
#     return encoded
#
#
# def decode_jwt(
#     jwt_token: str | bytes,
#     key: str = settings.auth.jwt_public_key.read_text(),
#     algorithm: str = settings.auth.algorithm,
# ):
#     decoded = jwt.decode(jwt=jwt_token, key=key, algorithms=[algorithm])
#
#     return decoded
#
#


async def authenticate_user(username: str, password: str, session: AsyncSession):
    unauthenticated = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user: User | None = await get_user_by_name(name=username, session=session)

    if user is None or not user.is_active or user.verify_password(password):
        raise unauthenticated

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + settings.auth.access_token_expires_delta, "iat": datetime.utcnow()})

    encoded_jwt = jwt.encode(to_encode, key=settings.auth.SECRET_KEY, algorithm=settings.auth.algorithm)
    return encoded_jwt
