from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant
from app.schemas.restaurant_schema import RestaurantCreate

def create_restaurant(db:Session, data:RestaurantCreate, owner_id:int):
    obj = Restaurant(
        name=data.name,
        description=data.description,
        owner_id=owner_id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_restaurants(db:Session):
    return db.query(Restaurant).all()

def get_restaurant_by_id(db:Session, restaurant_id:int):
    return db.query(Restaurant).filter(
        Restaurant.id == restaurant_id                                   
    ).first()
    
def delete_restaurant(db:Session, restaurant_id:int, owner_id:int):
    obj = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id, Restaurant.owner_id == owner_id
    ).first()

    if not obj:
        return None
    
    db.delete(obj)
    db.commit()
    return True