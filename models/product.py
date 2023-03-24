from decimal import Decimal

from config.database import Base
from sqlalchemy import DECIMAL, Column, Integer, String, Text


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(precision=9, scale=2), nullable=False, default=0.00)
    stock = Column(Integer, default=0)

    def __init__(self, name: str, description: str, price: Decimal):
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return (
            f"<Product id = {self.id}, name = {self.name}, description ="
            f" {self.description}, price = {self.price}>"
        )
