from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from .drivers.views import router as router_driver
from .orders.views import router as router_order

# from .config import Settings
from .db import db

app = FastAPI(
    title='API сервиса доставки Термокит'
)

# app.include_router(items_views.router)
# app.include_router(orders_views.router)
app.include_router(router_driver)
app.include_router(router_order)

# @lru_cache
# def get_settings():
#     return Settings()


# @app.get("/info")
# async def info(settings: Annotated[Settings, Depends(get_settings)]):
#     return {
#         "app_name": settings.app_name,
#         "db_driver": settings.db_driver,
#     }



