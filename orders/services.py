from typing import List
from core.database import db_session
from orders.models import OrderModel

class OrderDomainService:
    @staticmethod
    def get_order_by_id(order_id: int) -> OrderModel | None:
        """
        Retrieves a single order from the database by their unique ID.
        Returns None if no matching order is found.
        """
        return db_session.query(OrderModel).filter_by(id=order_id).first()
