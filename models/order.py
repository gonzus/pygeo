from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # 🛡️ String reference "UserModel" avoids immediate imports
    user: Mapped["UserModel"] = relationship(
        "UserModel",               # String name of the target class
        back_populates="orders", 
        lazy="raise"
    )
