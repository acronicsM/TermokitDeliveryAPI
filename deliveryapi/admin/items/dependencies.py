from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import db_helper, Item
from deliveryapi.admin.items import crud


async def item_by_id(
    item_id: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.sesion_dependency),
) -> Item:
    item = await crud.get_item(item_id=item_id, session=session)
    if item is not None:
        return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Позиция {item_id} не найден",
    )
