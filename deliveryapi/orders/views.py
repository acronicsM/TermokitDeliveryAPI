from fastapi import APIRouter

from .models import FAKE_ORDERS, FAKE_ITEMS

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/")
def get_orders(driver_id: int = None):
    if driver_id:
        return {k: v for k, v in FAKE_ORDERS.items() if v["driver"] == driver_id}
    return FAKE_ORDERS


@router.get("/{order_id}")
def get_order(order_id: str):
    if order_id in FAKE_ORDERS:
        return FAKE_ORDERS[order_id]

    return dict()


@router.get("/{order_id}/items")
def get_items(order_id: str):
    if order_id in FAKE_ITEMS:
        return FAKE_ITEMS[order_id]

    return dict()
