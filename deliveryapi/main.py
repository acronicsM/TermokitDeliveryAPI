from contextlib import asynccontextmanager

from fastapi import FastAPI

from deliveryapi.admin import router as router_admin
from deliveryapi.telegram.views import router as router_tg


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    {
        "name": "Load delivery",
        "description": "Загрузка данных из json",
    },
    {
        "name": "Telegram",
        "description": "Функции для работы водителей через телеграмм",
    },
]

app = FastAPI(
    title="API сервиса доставки Термокит",
    version="1.0",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(router_admin)
app.include_router(router_tg)
