from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cart_schema import AddToCart
from app.crud.cart_crud import add_to_cart, remove_from_cart, get_cart
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["Cart"])

# Add Item to Cart
@router.post("/add")
def add(data:AddToCart,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    
    return add_to_cart(db, current_user.id, data.menu_id, data.quantity)

# Remove Item from Cart
@router.delete("/remove/{menu_id}")
def remove(menu_id:int,
           db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):
    remove_from_cart(db, current_user.id, menu_id)
    return {"msg":"Removed"}

# Get Cart
@router.get("/")
def view_cart(db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    return get_cart(db, current_user.id)