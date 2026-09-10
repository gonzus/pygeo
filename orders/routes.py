from flask import request, jsonify
from orders import orders_bp
from .services import OrderDomainService

@orders_bp.route("<int:order_id>", methods=["GET"])
def get_order_details(order_id: int):
    """
    HTTP endpoint to get a single order's details: GET /orders/123
    """
    order = OrderDomainService.get_order_by_id(order_id)

    if not order:
        return jsonify({"error": f"Order with ID {order_id} not found"}), 404

    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "amount": order.amount,
    }), 200


@orders_bp.route("user/<int:user_id>", methods=["GET"])
def get_user_orders(user_id: int):
    """
    HTTP Entry Point: GET /orders/user/123
    Returns a list of all orders belonging to the specified user.
    """
    try:
        orders = OrderDomainService.get_orders_by_user_id(user_id)

        serialized_orders = [
            {
                "id": order.id,
                "amount": order.amount,
                "user_id": order.user_id
            }
            for order in orders
        ]

        return jsonify(serialized_orders), 200

    except Exception as err:
        return jsonify({"error": "Failed to retrieve user orders", "details": str(err)}), 500


@orders_bp.route("user/<int:user_id>", methods=["POST"])
def add_order_to_user(user_id: int):
    """
    HTTP Entry Point: POST /orders/user/123
    Payload Body JSON: {"amount": 54.50}
    """
    payload = request.get_json() or {}
    amount = payload.get("amount")

    if amount is None:
        return jsonify({"error": "Missing 'amount' field in request payload."}), 400

    try:
        order = OrderDomainService.create_order_for_user(user_id=user_id, amount=float(amount))

        return jsonify({
            "status": "success",
            "order": {
                "id": order.id,
                "user_id": order.user_id,
                "amount": order.amount
            }
        }), 201

    except ValueError as err:
        return jsonify({"error": str(err)}), 400
