from typing import TYPE_CHECKING

from sqlalchemy import String, TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .drivers import Driver


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(primary_key=True)
    orde_1c_number: Mapped[str] = mapped_column(String(11))
    id_search: Mapped[int]
    buyer: Mapped[str] = mapped_column(String(250))
    telephone: Mapped[str] = mapped_column(String(12))
    address: Mapped[str] = mapped_column(TEXT)
    comment: Mapped[str] = mapped_column(TEXT, nullable=True)
    delivered: Mapped[bool]

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
    )

    driver: Mapped["Driver"] = relationship(back_populates="orders")
