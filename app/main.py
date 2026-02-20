from fastapi import FastAPI
from app.routes import user_routes, restaurant_routes, menu_routes, cart_routes, order_routes, payment_routes, upload_routes, analytics_routes
from app.database import Base, engine
from fastapi.staticfiles import StaticFiles
import os

# create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Ordering Backend")

if not os.path.exists("app/uploads"):
    os.makedirs("app/uploads")

app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

app.include_router(user_routes.router)
app.include_router(restaurant_routes.router)
app.include_router(menu_routes.router)
app.include_router(cart_routes.router)
app.include_router(order_routes.router)
app.include_router(payment_routes.router)
app.include_router(upload_routes.router)
app.include_router(analytics_routes.router)

@app.get("/")
def home():
    return {"msg":"Food Ordering Backend Running"}