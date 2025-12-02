from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from typing import Union, Any
import os

from jose import jwt, JWTError
from passlib.context import CryptContext

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")  # CHANGE for prod
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

def hash_password(plain: str) -> str:
    # pbkdf2_sha256 does not have the 72-byte bcrypt limit and needs no external backend
    return pbkdf2_sha256.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(plain, hashed)

def create_access_token(
    subject: Union[str, int],
    expires_delta: timedelta | None = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=JWT_EXPIRE_MINUTES)

    to_encode: dict[str, Any] = {
        "sub": str(subject),
        "exp": datetime.utcnow() + expires_delta,
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt