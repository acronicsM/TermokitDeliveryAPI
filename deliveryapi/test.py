from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates")


class ItemBase(BaseModel):
    code_item: str
    article_item: str
    unit: str
    name: str
    quantity: float
    quantity_shipped: float
    price: float
    sum: float
    discount: float
    bonus: float


class OrderCart(BaseModel):
    id: int
    orde_1c_number: str


class ItemCart(ItemBase):
    id: int


class DriverCart(BaseModel):
    id: int


class Cart(BaseModel):
    driver: DriverCart
    order: OrderCart
    items: list[ItemCart]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get(
    path="/tg/123/orders/1/cart",
    response_class=HTMLResponse,
)
async def get_driver_order_items(
    request: Request,
):
    driver = DriverCart(id=123)
    order = OrderCart(id=1, orde_1c_number="yyyy")
    items = [
        ItemCart(
            id=1,
            code_item="c",
            article_item="a",
            unit="u",
            name="name",
            quantity=20,
            quantity_shipped=1,
            price=1,
            sum=1,
            discount=1,
            bonus=1,
        ),
        ItemCart(
            id=2,
            code_item="c",
            article_item="a",
            unit="u",
            name="name",
            quantity=20,
            quantity_shipped=1,
            price=1,
            sum=1,
            discount=1,
            bonus=1,
        ),
        ItemCart(
            id=3,
            code_item="c",
            article_item="a",
            unit="u",
            name="name",
            quantity=1,
            quantity_shipped=1,
            price=1,
            sum=1,
            discount=1,
            bonus=1,
        ),
    ]

    cart = Cart(driver=driver, order=order, items=items)

    return templates.TemplateResponse("test2.html", {"request": request, "cart": cart})


@app.post(
    path="/tg/123/orders/1/cart",
)
async def update_cart(request: Request):
    form_data = await request.form()
    print(form_data)
    return 200
