from fastapi import APIRouter

from .models import FAKE_DRIVERS

router = APIRouter(prefix='/drivers', tags=['Drivers'])


@router.get("/")
def get_drivers():
    return [{'id': id, 'name': value['name']} for id, value in FAKE_DRIVERS.items()]
