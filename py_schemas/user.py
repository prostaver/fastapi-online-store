from typing import Optional

from pydantic import BaseModel

from py_schemas.user_type import UserType


class BaseUser(BaseModel):
    username: str


class CreateUser(BaseUser):
    password: Optional[str]


class User(BaseUser):
    id: int
    user_type_id: int

    user_type: UserType

    class Config:
        orm_mode = True
