from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, User
from .schemas import UserInfo, UserCreate

from .dependencies import user_by_id
from . import crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/",
    description="Возвращает список всех пользователей",
    name="Список пользователей",
    response_model=list[UserInfo],
)
async def users(session: AsyncSession = Depends(db_helper.sesion_dependency)):
    return await crud.get_users(session)


@router.get(
    path="/{user_id}",
    description="Детальный данные о пользователе",
    name="Данные пользователя",
    response_model=UserInfo,
)
async def user_detail(user: User = Depends(user_by_id)):
    return user


@router.patch(
    path="/{user_id}",
    description="Установка активности пользователя",
    name="Активность пользователя",
    response_model=UserInfo | None,
)
async def auth_driver(
    is_active: bool,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.active_user(user=user, session=session, is_active=is_active)


@router.delete(
    path="/{user_id}",
    description="Производит удаление пользователя",
    name="Удаление пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.del_user(user=user, session=session)


@router.post(
    path="/new",
    description="Регистрация нового пользователя",
    name="Регистрация пользователя",
    response_model=UserInfo | None,
)
async def user_auth(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)
