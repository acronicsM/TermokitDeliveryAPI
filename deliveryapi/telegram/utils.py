from fastapi import status, HTTPException

from deliveryapi.core.models import Driver, Order, Item
from .schemas import ItemCart


def check_driver_order(order: Order, driver: Driver, search=False):
    if order.driver_id != driver.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Доставка {order.id_search if search else order.id} не найден",
        )

    return order


def model_to_schema(model: Driver | Order | Item, schema: ItemCart):
    # model_dict = model.__dict__.copy()
    # del model_dict["_sa_instance_state"]
    return schema(**{k: v for k, v in model.__dict__.items() if k != "_sa_instance_state"})
