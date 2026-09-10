from flask import request, jsonify
from orders import orders_bp
from .services import OrderDomainService

@orders_bp.route("<int:order_id>", methods=["GET"])
def get_order_details(order_id: int):
    """
    HTTP endpoint to get a single order's profile: GET /orders/123
    """
    # 1. Ask the service layer to look up the domain model
    order = OrderDomainService.get_order_by_id(order_id)

    # 2. Return a clean 404 error if the record does not exist
    if not order:
        return jsonify({"error": f"Order with ID {order_id} not found"}), 404

    # 3. Serialize the model properties explicitly (honoring lazy="raise")
    return jsonify({
        "id": order.id,
        "email": order.email,
        "name": order.name,
        "is_active": order.is_active
    }), 200
