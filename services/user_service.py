from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .hash_service import hash_password
from models import user as model_user
from py_schemas import user as user_schema
from py_schemas.user_type import UserTypes


def create_user(db: Session, user_input: user_schema.CreateUser):
    user_type = UserTypes.Shopper
    user_data = model_user.User(
        user_input.username,
        hash_password(user_input.password),
        user_type.value,
    )
    db.add(user_data)
    db.commit()

    return user_data


def update_user(db: Session, user_input: user_schema.CreateUser, user_id: int):
    user_data = (
        db.query(model_user.User).filter(model_user.User.id == user_id).first()
    )

    if not user_data:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No user found with id: {user_id}"
        )

    user_data.username = user_input.username
    if user_input.password:
        user_data.password = user_input.password

    db.add(user_data)
    db.commit()

    return user_data


def get_users(db: Session):
    return db.query(model_user.User).all()


def get_user(db: Session, user_id: int):
    user = (
        db.query(model_user.User).filter(model_user.User.id == user_id).first()
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No user found with id: {user_id}"
        )
    return user


def delete_user(db: Session, user_id: int):
    user = (
        db.query(model_user.User).filter(model_user.User.id == user_id).first()
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No user found with id: {user_id}"
        )

    db.delete(user)
    db.commit()

    return {"message": f"Successfully deleted user with id {user_id}"}


def get_user_by_username(db: Session, username: str):
    user = (
        db.query(model_user.User)
        .filter(model_user.User.username == username)
        .first()
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No user found with username: {username}",
        )
    return user
