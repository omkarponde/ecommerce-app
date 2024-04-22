from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class CreateOrderModel(BaseModel):
    order_data: List[List[int]]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "order_data": [[1, 2], [3, 4]]
            }
        }

class UpdateOrderModel(BaseModel):
    product_ids: List[int]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "product_ids": [1, 2]
            }
        }


class OrderResponseModel(BaseModel):
    id: int
    user_id: int
    price: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
