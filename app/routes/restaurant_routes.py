from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.restaurant_schema import RestaurantCreate, RestaurantResponse
from app.crud.restaurant_crud import (
    create_restaurant, get_restaurants,get_restaurant_by_id,delete_restaurant
)
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

# Restaurant Create
@router.post("/", response_model=RestaurantResponse)
def create(data:RestaurantCreate, db:Session =Depends(get_db),current_user: User = Depends(get_current_user)):
    return create_restaurant(db, data, current_user.id)

# Get all Restaurants
@router.get("/", response_model=List[RestaurantResponse])
def list_all(db:Session=Depends(get_db)):
    return get_restaurants(db)

# Get Restaurant By ID
@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_by_id(restaurant_id:int, db:Session= Depends(get_db)):
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return restaurant

# Delete Restaurant By ID
@router.delete("/{restaurant_id}")
def delete(restaurant_id:int,
           db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)
           ):
    
    delete = delete_restaurant(db, restaurant_id, current_user.id)

    if not delete:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return {"msg":"Restaurant deleted"}