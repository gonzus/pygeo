from flask import Blueprint
orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

from . import models
from . import routes

__all__ = ["orders_bp", "OrderDomainService"]
