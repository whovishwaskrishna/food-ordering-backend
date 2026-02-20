from pydantic import BaseModel,Field

class MenuCreate(BaseModel):
    name:str = Field(...,min_length=2, max_length=120)
    price:float = Field(..., gt=0)
    stock:int= Field(..., ge=0)    
    restaurant_id:int

class MenuUpdate(BaseModel):
    name:str | None = None
    price:float | None = None
    stock:int | None = None

class MenuResponse(BaseModel):
    id:int
    name:str
    price:float
    stock:int
    restaurant_id:int

    class Config:
        from_attributes = True
