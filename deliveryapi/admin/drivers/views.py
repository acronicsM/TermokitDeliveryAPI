from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Driver
from .schemas import DriverAuth, DriverCreate
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


# @router.post(
#     path="/registration",
#     description="Регистрация водителя",
#     name="Регистрация водителя",
#     responses={
#         200: {"description": "Вы зарегистрированы"},
#         401: {"description": "Ожидайте регистрации от администратора"},
#     },
# )
# async def drivers_auth(
#     driver_in: DriverCreate,
#     response: Response,
#     session: AsyncSession = Depends(db_helper.sesion_dependency),
# ):
#     if await crud.registration_driver(session=session, driver_in=driver_in):
#         response.status_code = status.HTTP_200_OK
#         return {"description": "Вы авторизованы"}
#
#     response.status_code = status.HTTP_401_UNAUTHORIZED
#     return {"description": "Ожидайте авторизации от администратора"}
