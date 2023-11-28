from fastapi import APIRouter

from deliveryapi.db import db


router = APIRouter(prefix='/{driver_id}/orders')

@router.get("/")
def get_orders(driver_id: int):
    orders = []
    if driver_id in db:
        orders = [{'order_id': order,
                   'number': db[driver_id][order]['id'],
                   'buyer': db[driver_id][order]['buyer'],
                   'telephone': db[driver_id][order]['telephone'],
                   'address': db[driver_id][order]['address'],
                   'comment': db[driver_id][order]['comment'],
                   } for order in db[driver_id]]

    return orders


@router.get("/{order_id}")
def get_order(driver_id: int, order_id: str):
    order = dict()

    if driver_id in db and order_id in db[driver_id]:
        _order = db[driver_id][order_id]
        order = {'order_id': order_id,
                 'number': _order['id'],
                 'buyer': _order['buyer'],
                 'telephone': _order['telephone'],
                 'address': _order['address'],
                 'comment': _order['comment'],
                 }

    return order
