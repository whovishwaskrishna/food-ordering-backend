from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.coupon import Coupon
from app.models.coupon_usage import CouponUsage

def apply_coupon(db: Session, user_id:int, code:str, order_total:float):
    coupon = db.query(Coupon).filter(
        Coupon.code == code,
        Coupon.is_active == True
    ).first()

    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid coupon")
    
    if coupon.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Coupon expired")
    
    if order_total < coupon.min_order:
        raise HTTPException(status_code=400, detail="Order too small for this coupon")
    
    used = db.query(CouponUsage).filter(
        CouponUsage.user_id == user_id,
        CouponUsage.coupon_id == coupon.id
    ).first()

    if used:
        raise HTTPException(status_code=400, detail="Coupon already used")
    
    # calculate discount
    if coupon.discount_type == "PERCENT":
        discount = order_total * (coupon.discount_value / 100)
        if coupon.mxa_discount:
            discount = min(discount, coupon.mxa_discount)
    else:
        discount = coupon.discount_value

    return discount, coupon