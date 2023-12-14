from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper
from .schemas import TokenSchema, DriverCreate
from .utils import authenticate_user, create_access_token
from . import crud


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    user = await authenticate_user(form_data.username, form_data.password, session=session)

    return TokenSchema(access_token=create_access_token(data={"sub": user.name}))


@router.post(
    path="/registration",
    description="Регистрация водителя",
    name="Регистрация водителя",
    responses={
        200: {"description": "Вы зарегистрированы"},
        401: {"description": "Ожидайте регистрации от администратора"},
    },
)
async def drivers_auth(
    driver_in: DriverCreate,
    response: Response,
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    if await crud.registration_driver(session=session, driver_in=driver_in):
        response.status_code = status.HTTP_200_OK
        return {"description": "Вы авторизованы"}

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"description": "Ожидайте авторизации от администратора"}
