from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from config.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    order_lines = relationship("OrderLine")

    def __init__(self, date: datetime, user_id: int) -> None:
        self.date = date
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"<Order id = {self.id}, date = {self.date}>"
