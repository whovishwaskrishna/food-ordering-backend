from sqlalchemy import Column,Integer,String,DateTime,Enum
from app.database import Base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime


class UserRole(str,enum.Enum):
    ADMIN="ADMIN"
    CUSTOMER="CUSTOMER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True,nullable=False,index=True)
    password = Column(String(200), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    created_at = Column(DateTime, default=datetime.utcnow)

    restaurants = relationship("Restaurant", back_populates="owner")
