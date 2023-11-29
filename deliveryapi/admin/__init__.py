from fastapi import APIRouter

from .drivers.views import router as driver_router


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)
router.include_router(router=driver_router)
