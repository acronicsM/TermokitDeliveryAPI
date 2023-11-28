from fastapi import APIRouter

from .models import FAKE_DRIVERS


router = APIRouter(prefix='/drivers', tags=['drivers'])


@router.get("/")
def get_orders():
    return [{'id': id, 'name': value['name']} for id, value in FAKE_DRIVERS.items()]

