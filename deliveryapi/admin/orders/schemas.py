from pydantic import BaseModel


class OrderBase(BaseModel):
    id: str
    orde_1c_number: str
    id_search: str
    buyer: str
    telephone: str
    address: str
    comment: str
    driver_id: str
    delivered: bool = False


class OrderCreate(OrderBase):
    pass
