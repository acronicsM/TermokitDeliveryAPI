from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper
from .schemas import Model
from . import crud

router = APIRouter(prefix="/upload", tags=["Load delivery"])


@router.post(
    path="/",
    description="Загружает данные доставок",
    name="Загрузка доставок",
    status_code=status.HTTP_200_OK,
)
async def upload(
    model_in: Model,
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    await crud.upload_deliveries(session=session, model_in=model_in)
