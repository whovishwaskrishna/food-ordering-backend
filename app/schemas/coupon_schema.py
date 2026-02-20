from pydantic import BaseModel

class ApplyCoupon(BaseModel):
    code:str