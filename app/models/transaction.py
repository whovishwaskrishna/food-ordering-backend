from sqlalchemy import Column, Integer,Float, ForeignKey, DateTime, String
from datetime import datetime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))

    amount = Column(Float, nullable=False)
    type = Column(String) # Wallet / Online
    status = Column(String, default="SUCCESS")

    created_at = Column(DateTime, default=datetime.utcnow)