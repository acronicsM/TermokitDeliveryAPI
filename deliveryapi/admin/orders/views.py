from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Order
from .schemas import OrderBase, OrderCreate
from .dependencies import order_by_id, order_by_id_search
from . import crud

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get(
    path="/",
    description="Возвращает список всех доставок",
    name="Список доставок",
    response_model=list[OrderBase],
)
async def get_orders(session: AsyncSession = Depends(db_helper.sesion_dependency)):
    orders = await crud.get_orders(session)
    return orders


@router.get(
    path="/{order_id}",
    description="Возвращает данные доставки по id",
    name="Доставка по id",
    response_model=OrderBase,
)
async def get_order_by_id(order: Order = Depends(order_by_id)):
    return order


@router.get(
    path="/search/{id_search}",
    description="Возвращает данные доставки по id_search",
    name="Доставка по id_search",
    response_model=OrderBase,
)
async def get_order_by_id_search(order: Order = Depends(order_by_id_search)):
    return order


@router.patch(
    path="/delivered/{order_id}",
    description="Установка признака доставки",
    name="Доставка",
    response_model=OrderBase,
)
async def auth_driver(
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.delivered_order(order=order, session=session)


@router.post(
    path="/",
    description="Создание доставки",
    name="Создание доставки",
    response_model=OrderBase,
)
async def create_order(
    order_in: OrderCreate,
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.create_order(order_in=order_in, session=session)


@router.delete(
    path="/{order_id}",
    description="Удаление доставки",
    name="Удаление доставки",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def auth_driver(
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.delivered_order(order=order, session=session)
