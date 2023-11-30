from sqlalchemy import select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import Driver
from .schemas import DriverBase, DriverCreate


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


async def create_driver(session: AsyncSession, driver_in: DriverCreate) -> Driver:
    driver = Driver(**driver_in.model_dump())
    session.add(driver)
    await session.commit()

    return driver


async def registration_driver(session: AsyncSession, driver_in: DriverCreate) -> bool:
    driver = await session.get(Driver, driver_in.id)
    if driver and driver.auth:
        return True

    await create_driver(session, driver_in)

    return False
