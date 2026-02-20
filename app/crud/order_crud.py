from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.menu import MenuItem
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.restaurant import Restaurant

ALLOWED_TRANSITIONS = {
    OrderStatus.PLACED: [OrderStatus.ACCEPTED, OrderStatus.CANCELLED],
    OrderStatus.ACCEPTED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
    OrderStatus.PREPARING: [OrderStatus.OUT_FOR_DELIVERY],
    OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: [],
}


def place_order(db: Session, user_id:int, coupon_code:str | None = None):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    if not items:
        raise HTTPException(status_code=400, detail="Cart empty")
    
    restaurant = db.query(Restaurant).filter(Restaurant.id == cart.restaurant_id).first()

    if not restaurant or not restaurant.is_open:
        raise HTTPException(status_code=400, detail="Restaurant closed")
    
    total = 0
    order_items = []

    # stock check + price calc
    for item in items:
        menu = db.query(MenuItem).filter(MenuItem.id == item.menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail="Menu item not found")


        if menu.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"{menu.name} out of stock")
        
        total += menu.price * item.quantity

        order_items.append({
            "menu":menu,
            "qty":item.quantity
        })

    # tax + delivery logic
    tax = total * 0.05
    delivery = 40 if total < 500 else 0

    subtotal = total + tax + delivery

    # coupon logic
    discount = 0
    coupon_obj = None

    if coupon_code:
        from app.crud.coupon_crud import apply_coupon
        discount, coupon_obj = apply_coupon(db, user_id, coupon_code, subtotal)

    final_total = subtotal - discount

    # create order
    order = Order(
        user_id = user_id,
        restaurant_id = cart.restaurant_id,
        total_amount = total,
        tax = tax,
        delivery_charge = delivery,
        grand_total = final_total
    )

    db.add(order)
    db.flush()

    # create order items + deduct stock
    for i in order_items:
        menu = i["menu"]
        qty = i["qty"]

        menu.stock -= qty

        oi = OrderItem(
            order_id = order.id,
            menu_id = menu.id,
            price = menu.price,
            quantity = qty
        )

        db.add(oi)

    # record coupon usage
    if coupon_obj:
        from app.models.coupon_usage import CouponUsage
        db.add(CouponUsage(user_id=user_id, coupon_id=coupon_obj.id))

    # clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()
    db.refresh(order)

    return order


def update_order_status(db: Session, order_id:int, new_status: OrderStatus):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    current = order.status

    # validate transition
    if new_status not in ALLOWED_TRANSITIONS[current]:
        raise HTTPException(status_code=400, detail=f"Invalid transition from {current} to {new_status}")
    
    order.status == new_status
    db.commit()
    db.refresh(order)

    return order