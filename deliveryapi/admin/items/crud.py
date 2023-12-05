from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import Item
from .schemas import ItemCreate


async def get_item(item_id: int, session: AsyncSession) -> Item | None:
    return await session.get(Item, item_id)


async def get_items(session: AsyncSession) -> list[Item]:
    result: Result = await session.execute(select(Item))
    items = list(result.scalars().all())
    return items


async def delete_item(session: AsyncSession, item: Item) -> None:
    await session.delete(item)
    await session.commit()


async def create_item(session: AsyncSession, item_in: ItemCreate) -> Item:
    item = Item(**item_in.model_dump())
    session.add(item)
    await session.commit()

    return item


async def delivered_item(session: AsyncSession, item: Item, quantity_shipped: float) -> Item:
    if quantity_shipped > item.quantity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quantity shipped cannot be greater than quantity",
        )
    elif quantity_shipped < 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quantity shipped must be greater than or equal to 0",
        )

    item.quantity_shipped = quantity_shipped
    await session.commit()

    return item
