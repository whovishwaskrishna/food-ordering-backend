from sqlalchemy import Column,Integer,String,Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name= Column(String(120), nullable=False)
    price= Column(Float,default=0)
    stock = Column(Integer, default=0)
    image_url = Column(String, nullable=True)

    restaurant_id= Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="menu_items")
