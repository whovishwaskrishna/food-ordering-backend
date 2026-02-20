from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.file_service import save_file
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["Upload"])

# Upload Restaurant Image
@router.post("/restaurant/{restaurant_id}")
def upload_restaurant_image(
    restaurant_id:int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        return {"error":"Restaurant not found"}
    
    if restaurant.owner_id != current_user.id:
        return {"error":"Not allowed"}
    
    path = save_file(file)

    restaurant.image_url = path
    db.commit()

    return {"image_url":path}


# Upload Menu Image
@router.post("/menu/{menu_id}")
def upload_menu_image(
    menu_id:int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(MenuItem).filter(MenuItem.id == menu_id).first()

    if not item:
        return {"error":"Menu item not found"}
    
    if item.restaurant.owner_id != current_user.id:
        return {"error":"Not allowed"}
    
    path = save_file(file)

    item.image_url = path
    db.commit()

    return {"image_url": path}