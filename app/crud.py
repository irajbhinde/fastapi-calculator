from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, security

def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    u = models.User(
        username=data.username,
        email=data.email,
        password_hash=security.hash_password(data.password),
    )
    db.add(u)
    db.flush()  # get PK early, raises on unique constraint
    return u

def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).get(user_id)
