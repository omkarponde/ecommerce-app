from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    seller = "seller"
    buyer = "buyer"
    guest = "guest"


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    role: str
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "user1",
                "email": "user1@example.com",
                "password": "password1",
                "role": "admin",
                "is_active": True
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "user1",
                "password": "password1",
            }
        }


class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "user1",
                "email": "user1@example.com",
                "password": "password1",
                "is_active": True
            }
        }


class UserResponseModel(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "id": 1,
                "username": "user1",
                "email": "user1@example.com",
                "role": "admin",
                "is_active": True,
                "created_at": "2024-04-12T18:30:53.351929",
                "updated_at": "2024-04-12T18:30:53.351938"
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = "40ff185794d8bea351ea33ae4eb1e1db580de8b020cb516742bd965ee7de4622"


class Token(BaseModel):
    access_token: str
    token_type: str
