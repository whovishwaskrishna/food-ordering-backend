from pydantic import BaseModel, Field

class AddToCart(BaseModel):
    menu_id:int
    quantity:int = Field(..., gt=0)

class cartItemResponse(BaseModel):
    menu_id: int
    quantity: int

    class Config:
        from_attributes = True