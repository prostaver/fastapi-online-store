import bcrypt

salt = b"$2b$12$GRJKLm1ig/Y4gimjR3GKm."


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
