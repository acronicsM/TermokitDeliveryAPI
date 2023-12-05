from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.models import Order, Item
from .schemas import Model
from ..drivers.crud import get_driver


async def upload_deliveries(model_in: Model, session: AsyncSession) -> None:
    for data in model_in.data:
        driver = await get_driver(driver_id=data.driver_id, session=session)
        if driver is None:
            continue

        for order_data in data.orders:
            stmt = select(Order).where(Order.driver_id == driver.id, Order.id_delivery == order_data.id_delivery)
            result: Result = await session.execute(stmt)

            if result.scalars().first():
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
