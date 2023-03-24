from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db_connection
from models.user import User
from py_schemas import order as order_schema
from routes.endpoints.user import get_current_user
from services import order_service


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get(
    "/",
    response_model=list[order_schema.Order],
    status_code=status.HTTP_200_OK,
)
async def get_orders(db: Session = Depends(get_db_connection)):
    return order_service.get_orders(db)


@router.get(
    "/{order_id}",
    response_model=order_schema.Order,
    status_code=status.HTTP_200_OK,
)
async def get_order(order_id: int, db: Session = Depends(get_db_connection)):
    return order_service.get_order(db, order_id)


@router.post(
    "/", response_model=order_schema.Order, status_code=status.HTTP_201_CREATED
)
async def create_order(
    order_input: order_schema.CreateOrder,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_connection),
):
    return order_service.create_order_from_schema(db, order_input, user)


@router.post(
    "/{order_id}",
    response_model=order_schema.Order,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_order(
    order_id: int,
    order_data: order_schema.CreateOrder,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_connection),
):
    return order_service.update_order(db, order_id, order_data, user)


@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_order(
    order_id: int, db: Session = Depends(get_db_connection)
):
    return order_service.delete_order(db, order_id)
