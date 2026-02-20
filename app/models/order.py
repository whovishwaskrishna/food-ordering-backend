from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class OrderStatus(str, enum.Enum):
    PLACED = "PLACED"
    ACCEPTED = "ACCEPTED"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    total_amount = Column(Float, nullable=False)
    tax = Column(Float, default=0)
    delivery_charge = Column(Float, default=0)
    grand_total = Column(Float, nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.PLACED, nullable=False)
    payment_status = Column(String, default="PENDING")
    paid_amount = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    restaurant = relationship("Restaurant")

    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

