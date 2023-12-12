from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Define SQLAlchemy models for the Cart and Item
Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    id_delivery = Column(String)
    id_search_delivery = Column(String)
    orde_1c_number = Column(String)
    id_search = Column(String)
    buyer = Column(String)
    telephone = Column(String)
    address = Column(String)
    comment = Column(String)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    code_item = Column(String)
    article_item = Column(String)
    unit = Column(String)
    name = Column(String)
    quantity = Column(Float)
    quantity_shipped = Column(Float)
    price = Column(Float)
    sum = Column(Float)
    discount = Column(Float)
    bonus = Column(Float)


# Connect to the database
engine = create_engine("sqlite:///cart.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Pydantic models
class OrderBase(BaseModel):
    id_delivery: str
    id_search_delivery: str
    orde_1c_number: str
    id_search: str
    buyer: str
    telephone: str
    address: str
    comment: str


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


class ItemShipped(BaseModel):
    id: int
    quantity_shipped: float


class OrderCart(BaseModel):
    id: int
    orde_1c_number: str


class ItemCart(ItemBase):
    id: int


class Cart(BaseModel):
    order: OrderCart
    items: list[ItemCart]


# Retrieve the Cart model from the database
def get_cart_from_db():
    db = SessionLocal()
    order = db.query(Order).first()
    items = db.query(Item).all()
    db.close()

    order_cart = OrderCart(id=order.id, orde_1c_number=order.orde_1c_number)
    items_cart = [ItemCart(id=item.id, **item.__dict__) for item in items]

    return Cart(order=order_cart, items=items_cart)


# Update the Cart model in the database
def update_cart_in_db(cart: Cart):
    db = SessionLocal()

    order = db.query(Order).filter(Order.id == cart.order.id).first()
    order.orde_1c_number = cart.order.orde_1c_number

    for item_cart in cart.items:
        item = db.query(Item).filter(Item.id == item_cart.id).first()
        item.quantity_shipped = item_cart.quantity_shipped

    db.commit()
    db.close()


# Endpoint to display and process the Cart form
@app.get("/")
def display_cart(request: Request):
    cart = get_cart_from_db()
    return templates.TemplateResponse("cart.html", {"request": request, "cart": cart})


@app.post("/")
def save_cart(request: Request, cart: Cart):
    update_cart_in_db(cart)
    return templates.TemplateResponse("cart.html", {"request": request, "cart": cart})


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
