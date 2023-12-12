from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper
from .schemas import TokenSchema
from .utils import authenticate_user, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_helper.sesion_dependency),
):
    user = await authenticate_user(form_data.username, form_data.password, session=session)

    return TokenSchema(access_token=create_access_token(data={"sub": user.name}))
