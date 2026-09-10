from typing import List
from core.database import db_session
from orders.models import OrderModel
from users.services import UserDomainService

class OrderDomainService:
    @staticmethod
    def get_order_by_id(order_id: int) -> OrderModel | None:
        """
        Retrieves a single order from the database by their unique ID.
        Returns None if no matching order is found.
        """
        return db_session.query(OrderModel).filter_by(id=order_id).first()


    @staticmethod
    def get_orders_by_user_id(user_id: int) -> List[OrderModel]:
        """
        Retrieves all orders matching a specific user ID from the database.
        Returns an empty list if the user has no orders or doesn't exist.
        """
        return (
            db_session.query(OrderModel)
            .filter(OrderModel.user_id == user_id)
            .all()
        )


    @staticmethod
    def create_order_for_user(user_id: int, amount: float) -> OrderModel:
        """
        Orchestrates cross-domain verification and persists a brand new order.
        """
        if not UserDomainService.is_user_eligible_for_orders(user_id):
            raise ValueError(f"Cannot place order: User {user_id} is inactive or does not exist.")

        if amount <= 0:
            raise ValueError("Order amount must be greater than zero.")

        new_order = OrderModel(user_id=user_id, amount=amount)

        db_session.add(new_order)
        db_session.commit()
        db_session.refresh(new_order)

        return new_order
