from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from models.user_type import UserType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    user_type_id = Column(Integer, ForeignKey("user_types.id"), nullable=False)

    user_type = relationship(UserType)

    def __init__(self, username: str, password: str, user_type_id: int):
        self.username = username
        self.password = password
        self.user_type_id = user_type_id

    def __repr__(self):
        return f"<User id = {self.id}, username = {self.username}>"
