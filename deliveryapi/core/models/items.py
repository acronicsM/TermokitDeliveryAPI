from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code_item: Mapped[str] = mapped_column(String(11), index=True)
    unit: Mapped[str] = mapped_column(String(5))
    name: Mapped[str]
    quantity: Mapped[float]
    quantity_shipped: Mapped[float]
    price: Mapped[float]
    sum: Mapped[float]
    discount: Mapped[float]
    bonus: Mapped[float]

    order_id: Mapped[str] = mapped_column(
        ForeignKey("orders.id"),
    )
