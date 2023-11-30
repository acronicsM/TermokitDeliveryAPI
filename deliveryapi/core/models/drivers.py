from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .orders import Order


class Driver(Base):
    __tablename__ = "drivers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    auth: Mapped[bool]

    orders: Mapped[list["Order"]] = relationship(back_populates="driver")
