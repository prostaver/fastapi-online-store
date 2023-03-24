import time

from fastapi import HTTPException, Response, status
from jose import jwt
from sqlalchemy.orm import Session

import services.user_service as user_service

from .hash_service import verify_password

SECRET_KEY = "c42dff633cc265f6444335d6094f87e309854b7c92f9b290c7d102d7a342adbc"
ALGORITHM = "HS256"


def create_auth_token(
    db: Session, username: str, password: str, response: Response
):
    user = user_service.get_user_by_username(db, username)
    if not verify_password(password, user.password):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Incorrect username or password",
            {"WWW-Authenticate": "Bearer"},
        )

    payload = {"username": user.username, "expiration": time.time() + 300000}

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    response.set_cookie(
        key="access_token", value=f"Bearer {token}", httponly=True
    )
    return {"access_token": token, "token_type": "bearer"}


def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return (
            decoded_token
            if decoded_token["expiration"] >= time.time()
            else None
        )
    except ValueError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid token.",
            {"WWW-Authenticate": "Bearer"},
        )
