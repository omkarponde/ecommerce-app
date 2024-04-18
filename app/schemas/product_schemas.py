from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional
from datetime import datetime


class CreateProductModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "name": "product1",
                "description": "This is product 1",
                "price": 99
            }
        }


class UpdateProductModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int] = Field()

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "name": "product1**",
                "description": "Updated desc",
                "price": 1000
            }
        }


class ProductResponseModel(BaseModel):
    id: int
    name: str
    description: str
    price: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "id": 1,
                "name": "product1",
                "description": "Updated desc",
                "price": 1000,
                "user_id": 1,
                "created_at": "2024-04-12T19:01:29.479403"
            }
        }
