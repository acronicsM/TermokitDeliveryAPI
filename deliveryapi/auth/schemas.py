from pydantic import BaseModel

from ..admin.drivers.schemas import DriverBase


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class DriverCreate(DriverBase):
    pass
