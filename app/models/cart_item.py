from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=True)
    menu_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)

    quantity = Column(Integer, default=1)
    
    cart = relationship("Cart", back_populates="items")
    menu = relationship("MenuItem")