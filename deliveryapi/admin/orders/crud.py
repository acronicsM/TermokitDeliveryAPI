from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import Order
from .schemas import OrderCreate


async def get_order(order_id: str, session: AsyncSession) -> Order | None:
    return await session.get(Order, order_id)


async def get_order_id_search(id_search: int, session: AsyncSession) -> Order | None:
    stmt = select(Order).where(Order.id_search == id_search)
    result: Result = await session.execute(stmt)
    result = result.scalars().one()
    return result


async def get_orders(session: AsyncSession) -> list[Order]:
    stmt = select(Order)
    result: Result = await session.execute(stmt)
    orders = list(result.scalars().all())
    return orders


async def delete_order(session: AsyncSession, order: Order) -> None:
    await session.delete(order)
    await session.commit()


async def create_order(session: AsyncSession, order_in: OrderCreate) -> Order:
    order = Order(**order_in.model_dump())
    session.add(order)
    await session.commit()

    return order


async def delivered_order(session: AsyncSession, order: Order) -> Order:
    order.delivered = True
    await session.commit()

    return order
