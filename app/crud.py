from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas, security
from .calculation_factory import CalculationFactory


# ---------------------------
# User CRUD
# ---------------------------


def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(
        username=data.username,
        email=data.email,
        password_hash=security.hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.username == username)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_identifier(db: Session, identifier: str) -> Optional[models.User]:
    """
    Identifier can be username OR email.
    """
    stmt = select(models.User).where(
        (models.User.username == identifier) | (models.User.email == identifier)
    )
    return db.execute(stmt).scalar_one_or_none()


def list_users(db: Session) -> Iterable[models.User]:
    stmt = select(models.User).order_by(models.User.id)
    return db.execute(stmt).scalars().all()


# ---------------------------
# Auth helpers
# ---------------------------


def verify_user_credentials(
    db: Session, data: schemas.UserLogin
) -> Optional[models.User]:
    user = get_user_by_identifier(db, data.identifier)
    if not user:
        return None
    if not security.verify_password(data.password, user.password_hash):
        return None
    return user


# ---------------------------
# Calculation CRUD
# ---------------------------


def create_calculation(
    db: Session, data: schemas.CalculationCreate
) -> models.Calculation:
    # choose operation via factory
    operation = CalculationFactory.create(data.type.value)
    result = operation(data.a, data.b)

    calc = models.Calculation(
        a=data.a,
        b=data.b,
        type=data.type.value,
        result=result,
        user_id=data.user_id,
        note=data.note,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def get_calculation(db: Session, calc_id: int) -> Optional[models.Calculation]:
    stmt = select(models.Calculation).where(models.Calculation.id == calc_id)
    return db.execute(stmt).scalar_one_or_none()


def list_calculations(db: Session) -> Iterable[models.Calculation]:
    stmt = select(models.Calculation).order_by(models.Calculation.id)
    return db.execute(stmt).scalars().all()


def update_calculation(
    db: Session, calc: models.Calculation, data: schemas.CalculationUpdate
) -> models.Calculation:
    if data.a is not None:
        calc.a = data.a
    if data.b is not None:
        calc.b = data.b
    if data.type is not None:
        calc.type = data.type.value
    if data.note is not None:
        calc.note = data.note

    # recompute result if a/b/type were changed
    if any([data.a is not None, data.b is not None, data.type is not None]):
        operation = CalculationFactory.create(calc.type)
        calc.result = operation(calc.a, calc.b)

    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def delete_calculation(db: Session, calc: models.Calculation) -> None:
    db.delete(calc)
    db.commit()
