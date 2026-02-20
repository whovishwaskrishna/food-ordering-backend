from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.menu import MenuItem

def add_to_cart(db:Session, user_id:int, menu_id:int, qty:int):
    menu = db.query(MenuItem).filter(MenuItem.id == menu_id).first()

    if not menu:
        raise HTTPException(404, "Menu item not found")
    
    if menu.stock < qty:
        raise HTTPException(400, "Not enough stock")
    
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    # create new cart if none
    if not cart:
        cart = Cart(user_id=user_id, restaurant_id=menu.restaurant_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # restaurant conflict check
    if cart.restaurant_id != menu.restaurant_id:
        raise HTTPException(400, "Cart contains items from another restaurant")
    
    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.menu_id == menu_id
    ).first()

    if item:
        item.quantity += qty
    else:
        item = CartItem(cart_id=cart.id, menu_id=menu_id, quantity=qty)
        db.add(item)

    db.commit()
    return cart

def remove_from_cart(db:Session, user_id:int, menu_id:int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return True
    
    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.menu_id == menu_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    return True

# def get_cart(db: Session, user_id:int):
#     return db.query(Cart).filter(Cart.user_id == user_id).first()

def get_cart(db: Session, user_id:int):
    cart=(db.query(Cart).options(joinedload(Cart.items).joinedload(CartItem.menu)).filter(Cart.user_id == user_id).first())

    if not cart:
        return None
    
    total = 0
    items_data = []

    for item in cart.items:
        price = item.menu.price
        subtotal = price * item.quantity
        total += subtotal

        items_data.append({
            "menu_id":item.menu_id,
            "name": item.menu.name,
            "price": price,
            "quantity":item.quantity,
            "subtotal": subtotal
        })

    return {
        "cart_id": cart.id,
        "restaurant_id": cart.restaurant_id,
        "items": items_data,
        "total_amount": total
    }
