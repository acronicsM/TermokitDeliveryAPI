from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Driver
from .schemas import DriverAuth
from .dependencies import driver_by_id
from . import crud

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.get(
    path="/",
    description="Возвращает список всех водителей",
    name="Список водителей",
    response_model=list[DriverAuth],
)
async def get_drivers(session: AsyncSession = Depends(db_helper.sesion_dependency)):
    drivers = await crud.get_drivers(session)
    return drivers


@router.patch(
    path="/{driver_id}",
    description="Установка признака аутентификации",
    name="Аутентификация водителя",
    response_model=DriverAuth | None,
)
async def auth_driver(
    driver: Driver = Depends(driver_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.auth_driver(driver=driver, session=session)


@router.delete(
    path="/{driver_id}",
    description="Производит удаление водителя",
    name="Удаление водителя",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def auth_driver(
    driver: Driver = Depends(driver_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.delete_driver(driver=driver, session=session)
