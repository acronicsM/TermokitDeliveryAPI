from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Driver, Order
from .schemas import OrderBase, ItemBase, ItemShipped

from ..admin.drivers.dependencies import driver_by_id
from ..admin.orders.dependencies import order_by_id, order_by_id_search
from . import crud

router = APIRouter(prefix="/tg/{driver_id}", tags=["Telegram"])


def check_driver_order(order: Order, driver: Driver, search=False):
    if order.driver_id != driver.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Доставка {order.id_search if search else order.id} не найден",
        )

    return order


@router.get(
    path="/",
    description="Возвращает список доставок по водителю",
    name="Список доставок",
    response_model=list[OrderBase],
)
async def get_driver_orders(
    driver: Driver = Depends(driver_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    orders = await crud.get_driver_orders(session=session, driver=driver)
    return orders


@router.get(
    path="/orders/{order_id}",
    description="Возвращает данные доставки водителя по id",
    name="Данные доставки по id",
    response_model=list[OrderBase],
)
async def get_driver_order(
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id),
):
    return check_driver_order(driver=driver, order=order)


@router.get(
    path="/orders/search/{search_id}",
    description="Возвращает данные доставки водителя по search_id",
    name="Данные доставки по search_id",
    response_model=list[OrderBase],
)
async def search_driver_order(
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id_search),
):
    return check_driver_order(driver=driver, order=order, search=True)


@router.post(
    path="/orders/shipped/{order_id}",
    description="Изменяет признак доставленной доставки",
    name="Доставка доставлена",
    status_code=status.HTTP_200_OK,
)
async def post_driver_order_shipped(
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    order = check_driver_order(driver=driver, order=order)
    await crud.get_driver_order_shipped(session=session, order=order)


@router.get(
    path="/orders/{order_id}/items",
    description="Возвращает список товаров доставки",
    name="Список товаров",
    response_model=list[ItemBase],
)
async def get_driver_order_items(
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    order = check_driver_order(driver=driver, order=order)
    items = await crud.get_driver_order_item(session=session, order=order)

    return items


@router.post(
    path="/orders/{order_id}/items",
    description="Изменяет доставленное количество товара",
    name="Доставленное количество",
    response_model=list[ItemBase],
)
async def post_driver_order_items(
    items: list[ItemShipped],
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    order = check_driver_order(driver=driver, order=order)
    await crud.items_shipped(session=session, items=items)
    items = await crud.get_driver_order_item(session=session, order=order)

    return items