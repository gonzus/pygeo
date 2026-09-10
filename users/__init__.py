from flask import Blueprint
users_bp = Blueprint("users", __name__, url_prefix="/api/users")

from . import models
from . import routes

__all__ = ["users_bp", "UserDomainService"]
