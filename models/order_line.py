from decimal import Decimal

from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Numeric


class OrderLine(Base):
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)
    amount = Column(Numeric(precision=9, scale=2), default=0)

    def __init__(
        self, order_id: int, product_id: int, quantity: int, amount: Decimal
    ) -> None:
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.amount = amount

    def __repr__(self) -> str:
        return (
            f"<OrderLine id = {self.id}, order_id = {self.order_id},"
            f" product_id = {self.product_id}, quantity = {self.quantity},"
            f" amount = {self.amount}>"
        )
