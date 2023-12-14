from pydantic import BaseModel


class DriverBase(BaseModel):
    id: int
    name: str
    auth: bool = False


class DriverAuth(DriverBase):
    pass


class DriverCreate(DriverBase):
    pass
