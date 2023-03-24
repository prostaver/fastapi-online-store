from typing import Optional
from decimal import Decimal

from pydantic import BaseModel


class BaseProduct(BaseModel):
    name: str
    description: str
    price: Optional[Decimal]


class CreateProduct(BaseProduct):
    pass


class Product(BaseProduct):
    id: int
    stock: int

    class Config:
        orm_mode = True
