from pydantic import BaseModel


class OrderBase(BaseModel):
    id: str
    id_delivery: str
    id_search_delivery: str
    orde_1c_number: str
    id_search: int
    buyer: str
    telephone: str
    address: str
    comment: str
    delivered: bool = False


class OrderCreate(OrderBase):
    pass
