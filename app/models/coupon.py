from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from app.database import Base

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(50), unique=True, nullable=False)
    discount_type = Column(String) # PERCENT / FLAT
    discount_value = Column(Float, nullable=False)

    min_order = Column(Float, default=0)
    mxa_discount = Column(Float, nullable=True)

    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)