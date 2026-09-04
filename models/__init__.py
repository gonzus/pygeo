from models.user import UserModel
from models.order import OrderModel

# This tells Python which classes are exported when someone runs "from models import *"
__all__ = ["UserModel", "OrderModel"]
