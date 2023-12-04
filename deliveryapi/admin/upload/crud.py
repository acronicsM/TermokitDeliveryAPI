from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.models import Order, Item
from .schemas import Model
from ..drivers.dependencies import driver_by_id
from ..orders.crud import get_order
from ..drivers.crud import get_driver


async def upload_deliveries(model_in: Model, session: AsyncSession) -> None:
    for data in model_in.data:
        driver = await get_driver(driver_id=data.driver_id, session=session)
        if driver is None:
            continue

        for order_data in data.orders:
            if await get_order(order_id=order_data.id, session=session):
                continue

            order_dict = order_data.model_dump()
            order_dict.pop("items")
            order = Order(**order_dict)
            order.driver_id = driver.id

            session.add(order)
            for item_data in order.items:
                item = Item(**item_data.model_dump())
                item.order_id = order.id

                session.add(item)

    await session.commit()
