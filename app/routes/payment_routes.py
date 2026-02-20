from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.crud.payment_crud import process_payment

router = APIRouter(prefix="/payment", tags=["Payment"])

# PAY ORDER API
@router.post("/{order_id}")
def pay(order_id:int, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    
    return process_payment(db, current_user.id, order_id)