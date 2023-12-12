from fastapi import APIRouter, Depends

from deliveryapi.auth.utils import get_current_active_user

from .drivers.views import router as driver_router
from .orders.views import router as order_router
from .items.views import router as item_router
from .upload.views import router as upload_router
from .users.views import router as user_router


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
router.include_router(router=driver_router)
router.include_router(router=order_router)
router.include_router(router=item_router)
router.include_router(router=upload_router)
router.include_router(router=user_router)
