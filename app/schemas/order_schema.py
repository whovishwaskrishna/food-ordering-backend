from pydantic import BaseModel
from app.models.order import OrderStatus

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(BaseModel):
    id:int
    total_amount:float
    tax:float
    delivery_charge:float
    grand_total:float
    status:str

    class Config:
        from_attributes = True