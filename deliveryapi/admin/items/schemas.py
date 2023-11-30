from pydantic import BaseModel


class OrderBase(BaseModel):
    id: str
    orde_1c_number: str
    id_search: int
    buyer: str
    telephone: str
    address: str
    comment: str
    driver_id: int
    delivered: bool = False


class OrderCreate(OrderBase):
    pass
