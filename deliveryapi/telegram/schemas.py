from pydantic import BaseModel


class OrderBase(BaseModel):
    id: str
    orde_1c_number: str
    id_search: int
    buyer: str
    telephone: str
    address: str
    comment: str


class ItemBase(BaseModel):
    id: int
    code_item: str
    unit: str
    name: str
    quantity: float
    quantity_shipped: float
    price: float
    sum: float
    discount: float
    bonus: float
    order_id: str


class ItemShipped(BaseModel):
    id: int
    quantity_shipped: float
