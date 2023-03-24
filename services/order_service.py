from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.cart import Cart
from models.order import Order
from models.order_line import OrderLine
from models.user import User
from py_schemas import order as order_schema
from py_schemas import order_line as ol_schema
from services import cart_service


def create_order_from_schema(
    db: Session, order_input: order_schema.CreateOrder, user: User
) -> None:
    order_data = Order(date=datetime.now(), user_id=user.id)

    db.add(order_data)
    db.commit()

    create_order_lines_from_schema(db, order_data.id, order_input.order_lines)


def update_order(
    db: Session,
    order_id: int,
    order_input: order_schema.CreateOrder,
    user: User,
) -> None:
    order_data: Order = get_order(db, order_id)

    if not order_data:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No order found with {order_id=}"
        )

    saved_ols = order_data.order_lines

    delete_order_lines(db, saved_ols)

    order_data.date = order_input.date
    db.add(order_data)
    db.commit()

    create_order_lines_from_schema(db, order_id, order_input.order_lines)


def get_order(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No order found with {order_id=}"
        )

    return order


def get_orders(db: Session) -> list[Order]:
    return db.query(Order).all()


def create_order_lines_from_schema(
    db: Session, order_id: int, order_lines: list[ol_schema.CreateOrderLine]
) -> None:
    for ol in order_lines:
        ol_data = OrderLine(order_id, ol.product_id, ol.quantity, ol.amount)
        db.add(ol_data)

    db.commit()


def delete_order_lines(db: Session, order_lines: list[OrderLine]) -> None:
    for ol in order_lines:
        db.delete(ol)
    db.commit()


def delete_order(db: Session, order_id: int) -> dict[str, str]:
    order_data = get_order(db, order_id)

    if not order_data:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No order found with {order_id=}"
        )

    delete_order_lines(db=db, order_lines=order_data.order_lines)

    db.delete(order_data)
    db.commit()

    return {"message": f"Successfully deleted order with id {order_id}"}


def create_order(db: Session, user: User) -> int:
    order_data = Order(date=datetime.now(), user_id=user.id)

    db.add(order_data)
    db.commit()

    return order_data.id


def save_order_lines(
    db: Session, cart_item_ids: list[int], order_id: int, user: User
):
    for cid in cart_item_ids:
        cart: Cart = cart_service.get_cart(db=db, user=user, cart_item_id=cid)
        order_line = cart.to_order_line(db=db, order_id=order_id)

        db.add(order_line)
        db.commit()


def check_out(db: Session, cart_item_ids: list[int], user: User):
    order_id = create_order(db, user)

    save_order_lines(
        db=db, cart_item_ids=cart_item_ids, order_id=order_id, user=user
    )
