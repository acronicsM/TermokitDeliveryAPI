import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)

    @staticmethod
    def hash_password(password: str | bytes):
        _password = password.encode("utf-8") if isinstance(password, str) else password

        return bcrypt.hashpw(_password, bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password=password.encode(), hashed_password=self.password)
