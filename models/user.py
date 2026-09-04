from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    # 🛡️ String reference "OrderModel" avoids immediate imports
    orders: Mapped[List["OrderModel"]] = relationship(
        "OrderModel",              # String name of the target class
        back_populates="user",
        lazy="raise"
    )
