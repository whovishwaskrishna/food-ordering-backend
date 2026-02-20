from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.menu import MenuItem
from app.models.restaurant import Restaurant
from app.schemas.menu_schema import MenuCreate, MenuUpdate
import json
from app.core.redis_client import redis_client

def create_menu_item(db:Session, data:MenuCreate, user_id:int):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == data.restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if restaurant.owner_id != user_id:
         raise HTTPException(status_code=403, detail="Not your Restaurant")
    
    obj = MenuItem(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    # delete cache
    redis_client.delete(f"menu:{obj.restaurant_id}")

    return obj

def update_menu_item(db: Session, item_id:int, data:MenuUpdate, user_id:int):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.restaurant.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    for key,value in data.dict(exclude_unset=True).items():
        setattr(item, key,value)

    db.commit()

    # delete cache
    redis_client.delete(f"menu:{item.restaurant_id}")

    db.refresh(item)
    return item

def delete_menu_item(db:Session, item_id:int, user_id:int):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.restaurant.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    db.delete(item)
    
    # delete cache
    redis_client.delete(f"menu:{item.restaurant_id}")

    db.commit()
    return True

def get_menu_by_restaurant(db:Session, restaurant_id:int):
    cache_key = f"menu:{restaurant_id}"
    cached = redis_client.get(cache_key)
    if cached:
        print("menu from cache")
        return json.loads(cached)
    
    items = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()

    data = [
        {
            "id":i.id,
            "name":i.name,
            "price":i.price,
            "stock":i.stock,
            "restaurant_id":i.restaurant_id
        }
        for i in items
    ]

    # cache 2 min
    redis_client.setex(cache_key,120, json.dumps(data))

    print("menu from DB")

    return data
    # return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()