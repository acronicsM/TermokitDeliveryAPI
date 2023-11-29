from pydantic import BaseModel


class DriverBase(BaseModel):
    id: int
    name: str
    auth: bool


class DriverAuth(DriverBase):
    pass
