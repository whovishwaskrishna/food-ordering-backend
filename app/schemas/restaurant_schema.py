from pydantic import BaseModel, Field
from typing import Optional

class RestaurantCreate(BaseModel):
    name:str = Field(..., min_length=2, max_length=100)
    description : Optional[str] = Field(None, max_length=255)

class RestaurantResponse(BaseModel):
    id:int
    name:str
    description:Optional[str]
    is_open:bool

    class Config:
        from_attributes = True