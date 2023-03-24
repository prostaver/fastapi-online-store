from decimal import Decimal

from pydantic import BaseModel


class BaseOrderLine(BaseModel):
    product_id: int
    quantity: int
    amount: Decimal


class CreateOrderLine(BaseOrderLine):
    pass


class OrderLine(BaseOrderLine):
    id: int
    order_id: int

    class Config:
        orm_mode = True
