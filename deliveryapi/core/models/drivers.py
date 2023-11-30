from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Driver(Base):
    __tablename__ = "drivers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    auth: Mapped[bool]
