from pydantic import BaseModel, EmailStr, ConfigDict

# Contract for data coming inside a POST request
class UserCreateSchema(BaseModel):
    email: EmailStr
    name: str

# Contract for data being formatted back out to the frontend
class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    name: str

    # Define model_config as a typed class dictionary attribute
    model_config = ConfigDict(from_attributes=True)


# Contract for updating an existing user profile (All fields optional)
class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
