from fastapi import status, HTTPException

from deliveryapi.core.models import Driver, Order


def check_driver_order(order: Order, driver: Driver, search=False):
    if order.driver_id != driver.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Доставка {order.id_search if search else order.id} не найден",
        )

    return order
