from contextlib import asynccontextmanager

from fastapi import FastAPI

from deliveryapi.core.models import Base, db_helper
from deliveryapi.telegram.views import router as router_driver
from deliveryapi.admin import router as router_admin


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
]

app = FastAPI(
    title="API сервиса доставки Термокит",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(router_driver)
app.include_router(router_admin)
