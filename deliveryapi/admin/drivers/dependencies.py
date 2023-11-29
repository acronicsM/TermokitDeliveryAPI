from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Driver
from deliveryapi.admin.drivers import crud


async def driver_by_id(
    driver_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.sesion_dependency),
) -> Driver:
    driver = await crud.get_driver(driver_id=driver_id, session=session)
    if driver is not None:
        return driver

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Водитель {driver_id} не найден",
    )
