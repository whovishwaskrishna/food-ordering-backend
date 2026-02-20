from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.analytics_crud import (
    get_total_revenue,
    get_total_orders,
    get_orders_per_day,
    top_restaurants,
    top_items
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# DASHBOARD SUMMARY
@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return {
        "revenue": get_total_revenue(db),
        "orders": get_total_orders(db)
    }

# ORDERS GRAPH DATA
@router.get("/order-per-day")
def orders_graph(db: Session = Depends(get_db)):
    return get_orders_per_day(db)

# TOP RESTAURANTS
@router.get("/top-restaurant")
def top_r(db: Session = Depends(get_db)):
    return top_restaurants(db)

# TOP ITEMS
@router.get("/top-items")
def top_i(db: Session = Depends(get_db)):
    return top_items(db)