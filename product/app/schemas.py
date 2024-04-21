from pydantic import BaseModel, Field
from pydantic.fields import Field
from typing import Optional
from datetime import datetime


class CreateProductModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: int = Field(..., gt=0)
    quantity_available: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "name": "product1",
                "description": "This is product 1",
                "price": 99,
                "quantity_available": 100
            }
        }


class UpdateProductModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int] = Field(..., gt=0)
    quantity_available: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "name": "product1**",
                "description": "Updated desc",
                "price": 1000,
                "quantity_available": 100
            }
        }


class ProductResponseModel(BaseModel):
    id: int
    name: str
    description: str
    price: int
    quantity_available: int
    user_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "id": 1,
                "name": "product1",
                "description": "Updated desc",
                "price": 1000,
                "quantity_available": 100,
                "user_id": 1
            }
        }
