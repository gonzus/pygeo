from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError  # <-- 1. Import the database error class
from sqlalchemy.orm import selectinload
from database import db_session 
from models.user import UserModel
from schemas.user_schema import UserCreateSchema, UserUpdateSchema, UserResponseSchema, UserSummaryResponseSchema

user_blueprint = Blueprint("users", __name__)

def init_user_blueprint(app, prefix: str):
    app.register_blueprint(user_blueprint, url_prefix=prefix)

@user_blueprint.route("", methods=["POST"])
def create_user() -> tuple[Response, int]:
    try:
        json_data = request.get_json() or {}
        validated_data = UserCreateSchema(**json_data)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422

    new_user = UserModel(
        email=validated_data.email,
        name=validated_data.name
    )
    try:
        db_session.add(new_user)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "A user with this email already exists."}), 409

    response_payload = UserResponseSchema.model_validate(new_user)
    return jsonify(response_payload.model_dump()), 201

@user_blueprint.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> tuple[Response, int]:
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = db_session.execute(stmt).scalar_one_or_none()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(UserResponseSchema.model_validate(user).model_dump()), 200

@user_blueprint.route("/summary", methods=["GET"])
def listing_endpoint():
    # Explicitly instruct SQLAlchemy to fetch the collection using an IN clause
    stmt = select(UserModel).options(selectinload(UserModel.orders))
    users = db_session.execute(stmt).scalars().all()
    serialized = [UserSummaryResponseSchema.model_validate(u).model_dump() for u in users]
    return jsonify(serialized)

@user_blueprint.route("", methods=["GET"])
def list_users() -> tuple[Response, int]:
    stmt = select(UserModel)
    users = db_session.execute(stmt).scalars().all()
    response_data = [UserResponseSchema.model_validate(u).model_dump() for u in users]
    return jsonify(response_data), 200

@user_blueprint.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> tuple[Response, int]:
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = db_session.execute(stmt).scalar_one_or_none()
    if not user:
        return jsonify({"error": "User not found"}), 404

    db_session.delete(user)
    db_session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@user_blueprint.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id: int) -> tuple[Response, int]:
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = db_session.execute(stmt).scalar_one_or_none()
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        json_data = request.get_json() or {}
        validated_data = UserUpdateSchema(**json_data)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422

    update_dict = validated_data.model_dump(exclude_unset=True)
    if not update_dict:
        return jsonify({"message": "No modification data provided"}), 200

    for key, value in update_dict.items():
        setattr(user, key, value)
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "This email address is already in use by another profile."}), 409

    response_payload = UserResponseSchema.model_validate(user)
    return jsonify(response_payload.model_dump()), 200
