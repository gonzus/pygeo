from pydantic import BaseModel, EmailStr

# Contract for data coming inside a POST request
class UserCreateSchema(BaseModel):
    email: EmailStr
    name: str

# Contract for data being formatted back out to the frontend
class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True  # Allows mapping directly out of SQLAlchemy objects

# Contract for updating an existing user profile (All fields optional)
class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
