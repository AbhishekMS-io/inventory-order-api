from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderItemResponse
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)



@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    product_ids = [
        item.product_id
        for item in order_data.items
    ]

    if len(product_ids) != len(set(product_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A product can only appear once in an order."
        )

    total_amount = Decimal("0.00")
    order_items = []


    try:
        for item in order_data.items:

            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .with_for_update()
                .first()
            )

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found."
                )

            if product.available_quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Insufficient inventory for product "
                        f"{product.id}. "
                        f"Available: {product.available_quantity}, "
                        f"requested: {item.quantity}."
                    )
                )

            subtotal = product.price * item.quantity

            total_amount += subtotal

            order_item = OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price
            )

            order_items.append(order_item)

            product.available_quantity -= item.quantity

        order = Order(
            total_amount=total_amount,
            items=order_items
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        return {
            "id": order.id,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.unit_price * item.quantity
                }
                for item in order.items
            ]
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order."
        )





@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

    return {
        "id": order.id,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.unit_price * item.quantity
            }
            for item in order.items
        ]
    }





@router.get(
    "",
    response_model=list[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db)
):
    orders = (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .all()
    )

    return [
        {
            "id": order.id,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.unit_price * item.quantity
                }
                for item in order.items
            ]
        }
        for order in orders
    ]