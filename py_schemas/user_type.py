from enum import Enum
from pydantic import BaseModel


class UserType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserTypes(Enum):
    Admin = 1
    Shopper = 2
