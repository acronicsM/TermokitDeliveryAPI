from contextlib import asynccontextmanager

from fastapi import FastAPI

from deliveryapi.core.models import Base, db_helper
from deliveryapi.admin import router as router_admin
from deliveryapi.telegram import router as router_tg


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


tags_metadata = [
    {
        "name": "Admin",
        "description": "Административные функции",
    },
    {
        "name": "Drivers",
        "description": "Функции работы с таблицей водителей",
    },
    {
        "name": "Orders",
        "description": "Функции работы с таблицей доставок",
    },
    {
        "name": "Items",
        "description": "Функции работы с таблицей позиций товаров",
    },
]

app = FastAPI(
    title="API сервиса доставки Термокит",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(router_admin)
app.include_router(router_tg)
