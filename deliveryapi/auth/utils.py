import jwt

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
