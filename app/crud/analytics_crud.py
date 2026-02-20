from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.menu import MenuItem
from app.models.restaurant import Restaurant

# TOTAL REVENUE
def get_total_revenue(db: Session):
    return db.query(func.sum(Order.total_amount)).scalar() or 0

# TOTAL ORDERS
def get_total_orders(db: Session):
    return db.query(func.count(Order.id)).scalar()

# ORDERS PER DAY
def get_orders_per_day(db: Session):
    data = db.query(
        func.date(Order.created_at),
        func.count(Order.id)
    ).group_by(func.date(Order.created_at)).all()

    return [{"date": str(d[0]), "orders": d[1]} for d in data]


# TOP RESTAURANTS BY REVENUE
def top_restaurants(db: Session):
    data = db.query(
        Restaurant.id,
        Restaurant.name,
        func.sum(Order.total_amount).label("revenue")
    ).join(Order, Order.restaurant_id == Restaurant.id).filter(Order.status != OrderStatus.CANCELLED).group_by(Restaurant.id, Restaurant.name).order_by(func.sum(Order.total_amount).desc()).limit(5).all()

    return [{"restaurant_id": d.id, "restaurant": d.name, "revenue": float(d.revenue or 0)} for d in data]

# TOP SELLING ITEMS
def top_items(db: Session):
    data = db.query(
        MenuItem.name,
        func.sum(OrderItem.quantity).label("sold")
    ).join(OrderItem, OrderItem.menu_id == MenuItem.id).group_by(MenuItem.name).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()

    return [{
        "item": d[0], "sold": int(d[1])
    } for d in data]
