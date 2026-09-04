from pydantic import BaseModel, EmailStr, ConfigDict, model_validator

# Contract for data coming inside a POST request
class UserCreateSchema(BaseModel):
    email: EmailStr
    name: str

# Contract for updating an existing user profile (all fields optional)
class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    name: str | None = None

# Contract for user being sent as response
class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str

# Contract for user summary being sent as response
class UserSummaryResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    total_orders: int = 0

    @model_validator(mode="before")
    @classmethod
    def calculate_total_orders(cls, data):
        if hasattr(data, "orders"):
            data.total_orders = len(data.orders)

        return data
