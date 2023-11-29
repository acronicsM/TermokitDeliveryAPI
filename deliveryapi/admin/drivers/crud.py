from sqlalchemy import select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import Driver


async def get_driver(driver_id: int, session: AsyncSession) -> Driver | None:
    return await session.get(Driver, driver_id)


async def get_drivers(session: AsyncSession) -> list[Driver]:
    stmt = select(Driver)
    result: Result = await session.execute(stmt)
    drivers = result.scalars().all()
    drivers = list(drivers)
    return drivers


async def auth_driver(driver: Driver, session: AsyncSession) -> Driver:
    driver.auth = True
    await session.commit()
    return driver


async def delete_driver(session: AsyncSession, driver: Driver) -> None:
    await session.delete(driver)
    await session.commit()
