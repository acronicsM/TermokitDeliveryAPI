from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserInfo(UserBase):
    is_active: bool
    id: int


class UserCreate(UserBase):
    password: str
