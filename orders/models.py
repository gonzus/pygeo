from sqlalchemy import Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="orders",
        lazy="raise"
    )
