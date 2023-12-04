from pydantic import BaseModel


class ItemBasis(BaseModel):
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


class ItemBase(ItemBasis):
    id: int


class ItemCreate(ItemBase):
    pass
