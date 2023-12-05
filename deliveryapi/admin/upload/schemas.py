from pydantic import BaseModel

from ..items.schemas import ItemWithID
from ..orders.schemas import OrderBase


class Order(OrderBase):
    items: list[ItemWithID]


class Delivery(BaseModel):
    driver_id: int
    orders: list[Order]


class Model(BaseModel):
    data: list[Delivery]
