from fastapi import APIRouter


router = APIRouter(
    prefix="/tg",
    tags=["Telegram"],
)
# router.include_router(router=driver_router)
# router.include_router(router=order_router)
# router.include_router(router=item_router)
