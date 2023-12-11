import jwt
import bcrypt

from ..core.config import settings


def encode_jwt(
    payload: dict,
    key: str = settings.auth.jwt_privet_key.read_text(),
    algorithm: str = settings.auth.algorithm,
):
    encoded = jwt.encode(payload=payload, key=key, algorithm=algorithm)

    return encoded


def decode_jwt(
    jwt_token: str | bytes,
    key: str = settings.auth.jwt_public_key.read_text(),
    algorithm: str = settings.auth.algorithm,
):
    decoded = jwt.decode(jwt=jwt_token, key=key, algorithms=[algorithm])

    return decoded


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
