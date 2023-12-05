from pydantic import BaseModel

from ..items.schemas import ItemBase
from ..orders.schemas import OrderBase


class Order(OrderBase):
    items: list[ItemBase]


class Delivery(BaseModel):
    driver_id: int
    orders: list[Order]


class Model(BaseModel):
    data: list[Delivery]
