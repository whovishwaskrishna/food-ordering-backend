from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.crud.order_crud import place_order, update_order_status
from app.schemas.order_schema import OrderResponse, OrderStatusUpdate
from app.models.order import OrderStatus
from app.services.notification_service import send_order_notification

router = APIRouter(prefix="/orders", tags=["Orders"])

class PlaceOrderRequest(BaseModel):
    coupon_code:str | None = None

# place order
@router.post("/place", response_model=OrderResponse)
def place(
    data: PlaceOrderRequest,
    background_tasks:BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    order = place_order(db, current_user.id, data.coupon_code)

    # background notification
    background_tasks.add_task(
        send_order_notification,
        order.id,
        current_user.email
    )

    return order


# Update Status for Order
@router.put("/{order_id}/status",response_model=OrderResponse)
def update_status(
    order_id:int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db)
    ):

    return update_order_status(db, order_id, data.status)
