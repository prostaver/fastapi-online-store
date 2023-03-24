from datetime import datetime

from pydantic import BaseModel

from .order_line import CreateOrderLine, OrderLine


class BaseOrder(BaseModel):
    user_id: int


class CreateOrder(BaseOrder):
    order_lines: list[CreateOrderLine] | None


class Order(BaseOrder):
    id: int
    date: datetime
    order_lines: list[OrderLine]

    class Config:
        orm_mode = True
