from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.models import db_helper
from .schemas import DriverBase, DriverCreate
from . import crud

router = APIRouter(prefix="/tg", tags=["Telegram"])


@router.post(
    path="/auth",
    description="Авторизация водителя",
    responses={
        200: {"description": "Вы авторизованы"},
        401: {"description": "Ожидайте авторизации от администратора"},
    },
)
async def drivers_auth(
    driver_in: DriverCreate,
    response: Response,
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    if await crud.auth_driver(session=session, driver_in=driver_in):
        response.status_code = status.HTTP_200_OK
        return {"description": "Вы авторизованы"}

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"description": "Ожидайте авторизации от администратора"}


@router.get(
    path="/{driver_id}",
    description="Получить список всех заказов водителя",
)
def get_drivers_orders(driver_id: int):
    # return {
    #     id: order for id, order in FAKE_ORDERS.items() if order["driver"] == driver_id
    # }
    return True


@router.get(
    path="/{driver_id}/{order_id}",
    description="Получить данные заказа",
)
def get_drivers_order(driver_id: int, order_id: str):
    # if order_id in FAKE_ORDERS and FAKE_ORDERS[order_id]["driver"] == driver_id:
    #     return FAKE_ORDERS[order_id]

    return dict()


@router.post(
    path="/{driver_id}/{order_id}/taken",
    description='Установка признака "заказ доставлен"',
)
def drivers_order_taken(driver_id: int, order_id: int):
    return True


@router.get(
    path="/{driver_id}/{order_id}/items",
    description="Получить список товаров заказа",
)
def get_drivers_order_items(driver_id: int, order_id: int):
    return True


@router.post(
    path="/{driver_id}/{order_id}/items/{item_id}",
    description="Установить доставленое количество товара",
)
def drivers_order_item_taken(driver_id: int, order_id: int, item_id: int):
    return True
