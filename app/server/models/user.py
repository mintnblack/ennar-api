from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UsersSchema(BaseModel):
    name: str = Field(...)
    username: EmailStr = Field(...)
    phone: str = Field(...)
    password: str = Field(...)
    disabled: bool = Field(default=False)
    created: datetime = Field(default=datetime.now())
    updated: datetime = Field(default=datetime.now())


class UpdateUserSchema(BaseModel):
    name: str = Field(default=None)
    disabled: bool = Field(default=None)
    updated: datetime = Field(default=datetime.now())


class UpdatePasswordSchema(BaseModel):
    password: str = Field(...)
    new_password: str = Field(...)
    username: str = Field(...)


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "username": user["username"],
        "phone": user["phone"],
        "disabled": user["disabled"],
        "created": user["created"],
        'updated': user["updated"]
    }


def user_auth_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "username": user["username"],
        "phone": user["phone"],
        "password": user["password"],
        "disabled": user["disabled"],
        "created": user["created"],
        'updated': user["updated"]
    }


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
