from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Driver, Order
from .schemas import OrderBase, ItemBase, ItemShipped

from ..admin.drivers.dependencies import driver_by_id
from ..admin.orders.dependencies import order_by_id, order_by_id_search, order_by_id_search_delivery
from . import crud, utils

router = APIRouter(prefix="/tg/{driver_id}", tags=["Telegram"])

templates = Jinja2Templates(directory="templates")


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
    response_model=OrderBase,
)
async def get_driver_order(
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id),
):
    return utils.check_driver_order(driver=driver, order=order)


@router.get(
    path="/orders/search/id/{search_id}",
    description="Возвращает данные доставки водителя по search_id",
    name="Данные доставки по search_id",
    response_model=OrderBase,
)
async def search_driver_order(
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id_search),
):
    return utils.check_driver_order(driver=driver, order=order, search=True)


@router.get(
    path="/orders/search/id_delivery/{id_search_delivery}",
    description="Возвращает данные доставки водителя по id_search_delivery",
    name="Данные доставки по id_search_delivery",
    response_model=OrderBase,
)
async def search_driver_delivery(
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id_search_delivery),
):
    return utils.check_driver_order(driver=driver, order=order, search=True)


@router.post(
    path="/orders/shipped/{order_id}",
    description="Изменяет признак доставленной доставки",
    name="Доставка доставлена",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def post_driver_order_shipped(
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    order = utils.check_driver_order(driver=driver, order=order)
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
    order = utils.check_driver_order(driver=driver, order=order)
    items = await crud.get_driver_order_item(session=session, order=order)

    return items


@router.get(
    path="/orders/{order_id}/cart",
    description="Открывает страницу корзины",
    name="Корзина",
    response_class=HTMLResponse,
)
async def get_driver_order_items(
    request: Request,
    driver: Driver = Depends(driver_by_id),
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    order = utils.check_driver_order(driver=driver, order=order)
    items = await crud.get_driver_order_item(session=session, order=order)

    return templates.TemplateResponse("cart.html", {"request": request, "items": items})


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
    order = utils.check_driver_order(driver=driver, order=order)
    await crud.items_shipped(session=session, items=items)
    items = await crud.get_driver_order_item(session=session, order=order)

    return items
