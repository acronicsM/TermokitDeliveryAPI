from sqlalchemy.ext.asyncio import AsyncSession

from ..core.models import Driver
from .schemas import DriverCreate


async def create_driver(session: AsyncSession, driver_in: DriverCreate) -> Driver:
    driver = Driver(**driver_in.model_dump())
    session.add(driver)
    await session.commit()

    return driver


async def auth_driver(session: AsyncSession, driver_in: DriverCreate) -> bool:
    driver = await session.get(Driver, driver_in.id)
    if driver and driver.auth:
        return True

    await create_driver(session, driver_in)

    return False
