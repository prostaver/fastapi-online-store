from decimal import Decimal

from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import Session

from config.database import Base
from models.order_line import OrderLine
from services import product_service


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)

    def __init__(self, user_id: int, product_id: int, quantity: int) -> None:
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self) -> str:
        return (
            f"<Cart id = {self.id} user_id = {self.user_id}, "
            f"product_id = {self.product_id}, quantity = {self.quantity}>"
        )

    def to_order_line(self, db: Session, order_id: int) -> OrderLine:
        product_amt = product_service.calculate_amount(
            db=db, product_id=self.product_id, quantity=self.quantity
        )

        order_line = OrderLine(
            order_id=order_id,
            product_id=self.product_id,
            quantity=self.quantity,
            amount=product_amt,
        )

        return order_line
