from pydantic import BaseModel


class OrderBase(BaseModel):
    id_delivery: str
    id_search_delivery: str
    orde_1c_number: str
    id_search: str
    buyer: str
    telephone: str
    address: str
    comment: str
    delivered: bool = False


class OrderWithID(OrderBase):
    id: int


class OrderCreate(OrderBase):
    driver_id: int
