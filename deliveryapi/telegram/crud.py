from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import Driver, Order, Item
from ..admin.items.dependencies import item_by_id
from .schemas import OrderBase, ItemBase, ItemShipped


async def get_driver_orders(session: AsyncSession, driver: Driver) -> list[OrderBase]:
    stmt = select(Order).join(Driver).where(Order.delivered == False, Driver.id == driver.id)
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()
    orders = list(orders)
    return orders


async def get_driver_order_shipped(session: AsyncSession, order: Order) -> None:
    order.delivered = True

    await session.commit()


async def get_driver_order_item(session: AsyncSession, order: Order) -> list[ItemBase]:
    stmt = select(Item).join(Order).where(Order.id == order.id)

    result: Result = await session.execute(stmt)
    items = result.scalars().all()
    items = list(items)
    return items


async def items_shipped(
    session: AsyncSession,
    items: list[ItemShipped],
) -> None:
    for i in items:
        item = await item_by_id(item_id=i.id, session=session)

        if i.quantity_shipped > item.quantity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quantity shipped cannot be greater than quantity",
            )
        elif i.quantity_shipped < 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quantity shipped must be greater than or equal to 0",
            )

        item.quantity_shipped = i.quantity_shipped

    await session.commit()
