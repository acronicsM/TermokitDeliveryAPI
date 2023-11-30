from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Order
from deliveryapi.admin.orders import crud


async def order_by_id(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.sesion_dependency),
) -> Order:
    order = await crud.get_order(order_id=order_id, session=session)
    if order is not None:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Доставка {order_id} не найден",
    )


async def order_by_id_search(
    id_search: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.sesion_dependency),
) -> Order:
    order = await crud.get_order_id_search(id_search=id_search, session=session)
    if order is not None:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Доставка {id_search} не найден",
    )
