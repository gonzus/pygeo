from flask import request, jsonify
from users import users_bp
from .services import UserDomainService

@users_bp.route("<int:user_id>", methods=["GET"])
def get_user_details(user_id: int):
    """
    HTTP endpoint to get a single user's profile: GET /users/123
    """
    # 1. Ask the service layer to look up the domain model
    user = UserDomainService.get_user_by_id(user_id)

    # 2. Return a clean 404 error if the record does not exist
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    # 3. Serialize the model properties explicitly (honoring lazy="raise")
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "is_active": user.is_active
    }), 200


@users_bp.route("", methods = ["POST"])
def register_user():
    payload = request.get_json() or {}

    try:
        # Delegate payload values straight to the business layer
        new_user = UserDomainService.create_user(
            email = payload.get("email", ""),
            name = payload.get("name", "")
        )

        return jsonify({
            "status": "success",
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "name": new_user.name,
                "is_active": new_user.is_active
            }
        }), 201
    except ValueError as err:
        # TODO: these could be different error codes:
        #   409: repeated email / name
        #   422: invalid email / name
        # Catch business constraints and translate them directly into clear HTTP error responses
        return jsonify({"error": str(err)}), 400


@users_bp.route("<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    """
    HTTP endpoint to permanently purge a user row: DELETE /users/123
    """
    # 1. Trigger the real SQL delete operation inside the service
    result = UserDomainService.delete_user_by_id(user_id)

    # 2. Map the service result tokens to explicit HTTP status codes
    if result == "not_found":
        return jsonify({"error": f"User with ID {user_id} does not exist."}), 404

    if result == "has_dependent_orders":
        return jsonify({
            "error": "Cannot delete user.",
            "details": f"User ID {user_id} still has active orders in the database. "
                       f"You must delete those orders first."
        }), 400

    # 3. Successful database deletion confirmation
    return jsonify({
        "status": "success",
        "message": f"User row with ID {user_id} was permanently deleted from the database."
    }), 200


@users_bp.route("", methods=["GET"])
def list_users():
    """
    HTTP endpoint to retrieve the list of all active users.
    """
    try:
        # 1. Fetch the domain objects from the service layer
        users = UserDomainService.get_all_users()

        # 2. Serialize the models safely into a plain list of dictionaries.
        # We explicitly omit the 'orders' relationship here to honor your `lazy="raise"` configuration.
        user_list = [
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "is_active": user.is_active
            }
            for user in users
        ]

        return jsonify(user_list), 200

    except Exception as err:
        # Catch unforeseen errors and format them safely
        return jsonify({"error": "Failed to retrieve users", "details": str(err)}), 500


@users_bp.route("search", methods=["GET"])
def search_users():
    """
    HTTP endpoint to search users via query parameter: GET /users/search?q=gonzo
    """
    # 1. Extract the search term from the HTTP request query parameters
    query_param = request.args.get("q", "")

    try:
        # 2. Delegate searching to the domain service layer
        matching_users = UserDomainService.search_users_by_name(query_param)

        # 3. Safely serialize results to a list of dicts (honoring lazy="raise")
        results = [
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "is_active": user.is_active
            }
            for user in matching_users
        ]

        return jsonify(results), 200

    except Exception as err:
        return jsonify({"error": "An error occurred during search", "details": str(err)}), 500
