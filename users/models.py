from typing import List
from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    orders: Mapped[List["OrderModel"]] = relationship(
        "OrderModel",
        back_populates="user",
        lazy="raise"
    )
