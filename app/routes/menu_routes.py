from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.menu_schema import MenuCreate, MenuResponse, MenuUpdate
from app.crud.menu_crud import (
    create_menu_item,
    update_menu_item,
    delete_menu_item,
    get_menu_by_restaurant
)
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/menu", tags=["Menu"])

# create Menu
@router.post("/", response_model=MenuResponse)
def create(data:MenuCreate,
           db:Session = Depends(get_db),
           current_user:User= Depends(get_current_user)):
    return create_menu_item(db,data, current_user.id)

# Update Menu
@router.put("/{item_id}", response_model=MenuResponse)
def update(item_id:int,
           data:MenuUpdate,
           db:Session=Depends(get_db),
           current_user:User=Depends(get_current_user)):
    return update_menu_item(db, item_id, data, current_user.id)

# Delete Menu
@router.delete("/{item_id}")
def delete(item_id:int,
           db: Session = Depends(get_db),
           current_user: User= Depends(get_current_user)):
    
    delete_menu_item(db,item_id,current_user.id)
    return {"msg":"Item Deleted"}

# Get Restaurant all Menu
@router.get("/{restaurant_id}", response_model=List[MenuResponse])
def list_menu(restaurant_id:int, db: Session = Depends(get_db)):
    return get_menu_by_restaurant(db, restaurant_id)