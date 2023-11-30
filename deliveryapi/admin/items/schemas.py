from pydantic import BaseModel


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


class ItemCreate(ItemBase):
    pass
