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


class ItemBase(BaseModel):
    code_item: str
    article_item: str
    unit: str
    name: str
    quantity: float
    quantity_shipped: float
    price: float
    sum: float
    discount: float
    bonus: float


class ItemShipped(BaseModel):
    id: int
    quantity_shipped: float
