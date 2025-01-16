from fastapi import APIRouter, HTTPException
from infrastructure.repositories import InMemoryOrderRepository
from application.dto import OrderDTO
from domain.models import Order
from typing import List

router = APIRouter()

# Repositories
order_repository = InMemoryOrderRepository()


@router.post("/orders", response_model=OrderDTO)
def create_order(order: OrderDTO):
    new_order = Order(order_id=order.order_id, user_id=order.user_id, details=order.details)
    return order_repository.create_order(new_order)


@router.get("/orders/{order_id}", response_model=OrderDTO)
def get_order(order_id: str):
    order = order_repository.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/orders", response_model=List[OrderDTO])
def list_orders():
    return order_repository.list_orders()
