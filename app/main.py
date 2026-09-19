from fastapi import FastAPI

from app.database import Base, engine
from app.models import Product, Order, OrderItem

from app.routers.products import router as products_router
from app.routers.orders import router as orders_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Inventory & Order Management API",
    description="Backend API for managing products, inventory and orders.",
    version="1.0.0"
)


app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "message": "Inventory & Order Management API is running"
    }


@app.get("/test-db")
def test_db():
    try:
        with engine.connect():
            return {
                "message": "Database connected successfully"
            }
    except Exception as e:
        return {
            "error": str(e)
        }

@app.get("/health")
def health_check():
    return {"status": "ok"}