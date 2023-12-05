from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Item
from .schemas import ItemWithID, ItemCreate
from .dependencies import item_by_id
from . import crud

router = APIRouter(prefix="/items", tags=["Items"])


@router.get(
    path="/",
    description="Возвращает список всех позиций",
    name="Список позиций",
    response_model=list[ItemWithID],
)
async def get_items(session: AsyncSession = Depends(db_helper.sesion_dependency)):
    items = await crud.get_items(session)
    return items


@router.get(
    path="/{item_id}",
    description="Возвращает данные позиции по id",
    name="Позиция по id",
    response_model=ItemCreate,
)
async def get_item_by_id(item: Item = Depends(item_by_id)):
    return item


@router.patch(
    path="/{item_id}/shipped",
    description="Установка доставленного количества",
    name="Доставка",
    response_model=ItemWithID,
)
async def shipped_item(
    quantity_shipped: float,
    item: Item = Depends(item_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.delivered_item(
        item=item, quantity_shipped=quantity_shipped, session=session
    )


@router.post(
    path="/",
    description="Создание позиции доставки",
    name="Создание позиции",
    response_model=ItemCreate,
)
async def create_order(
    item_in: ItemCreate,
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.create_item(item_in=item_in, session=session)


@router.delete(
    path="/{item_id}",
    description="Удаление позиции доставки",
    name="Удаление позиции",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_item(
    item: Item = Depends(item_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.delete_item(item=item, session=session)
