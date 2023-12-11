import bcrypt
from pydantic import BaseModel, SecretStr


class UserBase(BaseModel):
    name: str


class UserInfo(UserBase):
    is_active: bool
    id: int


class UserCreate(UserBase):
    password: str
