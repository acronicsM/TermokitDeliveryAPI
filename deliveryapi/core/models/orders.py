from sqlalchemy import String, Integer, TEXT, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(primary_key=True)
    orde_1c_number: Mapped[str] = mapped_column(String(11))
    id_search: Mapped[int] = mapped_column(Integer)
    buyer: Mapped[str] = mapped_column(String(250))
    telephone: Mapped[str] = mapped_column(String(12))
    address: Mapped[str] = mapped_column(TEXT)
    comment: Mapped[str] = mapped_column(TEXT, nullable=True)
    driver_id: Mapped[int] = mapped_column(Integer)
    delivered: Mapped[bool] = mapped_column(BOOLEAN)
