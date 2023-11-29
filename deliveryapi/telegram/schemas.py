from pydantic import BaseModel


class DriverBase(BaseModel):
    id: int
    name: str


class DriverCreate(DriverBase):
    auth: bool = False
