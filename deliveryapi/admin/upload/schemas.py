from pydantic import BaseModel

from ..items.schemas import ItemBasis
from ..orders.schemas import OrderBase


class Order(OrderBase):
    items: list[ItemBasis]


class Delivery(BaseModel):
    driver_id: int
    orders: list[Order]


class Model(BaseModel):
    data: list[Delivery]
