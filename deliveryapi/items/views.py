from fastapi import APIRouter

from deliveryapi.db import db


router = APIRouter(prefix='/{driver_id}/orders/{order_id}/items')


@router.get("/")
def get_order_items(driver_id: int, order_id: str):
    items = []

    if driver_id in db and order_id in db[driver_id]:
        items = db[driver_id][order_id]['items']

    return items
