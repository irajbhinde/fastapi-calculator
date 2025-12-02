# app/crud.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas, security
from .calculation_factory import CalculationFactory


# =========================
# User CRUD / Auth
# =========================

def get_user_by_username(db: Session, username: str):
    stmt = select(models.User).where(models.User.username == username)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_email(db: Session, email: str):
    stmt = select(models.User).where(models.User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=security.hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# M12-style login (for /users/login, used by integration tests)
def verify_user_credentials(db: Session, login_in: schemas.UserLogin):
    """
    Accepts 'identifier' which can be username OR email.
    """
    # Try username
    user = get_user_by_username(db, login_in.identifier)
    if not user:
        # Fallback to email
        user = get_user_by_email(db, login_in.identifier)
    if not user:
        return None

    if not security.verify_password(login_in.password, user.password_hash):
        return None

    return user


# M13 JWT login (for /login, used by frontend)
def verify_user_credentials_email(db: Session, login_in: schemas.JwtLogin):
    user = get_user_by_email(db, login_in.email)
    if not user:
        return None

    if not security.verify_password(login_in.password, user.password_hash):
        return None

    return user


# =========================
# Calculation CRUD
# =========================

def create_calculation(
    db: Session,
    calc_in: schemas.CalculationCreate,
) -> models.Calculation:
    """
    Create a calculation record, computing the result via CalculationFactory.
    """
    # calc_in.type is CalculationType (Enum), use it directly with the factory
    result = CalculationFactory.calculate(calc_in.a, calc_in.b, calc_in.type)

    db_calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type.value,  # store "add", "subtract", etc.
        result=result,
        note=calc_in.note,
        user_id=calc_in.user_id,
    )
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


def list_calculations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Calculation]:
    return (
        db.query(models.Calculation)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_calculation(db: Session, calculation_id: int) -> models.Calculation | None:
    return (
        db.query(models.Calculation)
        .filter(models.Calculation.id == calculation_id)
        .first()
    )


def update_calculation(
    db: Session,
    db_calc: models.Calculation,
    calc_update: schemas.CalculationUpdate,
) -> models.Calculation:
    """
    Apply partial update and recompute result if a/b/type changed.
    """
    # Track whether we need to recompute result
    dirty = False

    if calc_update.a is not None:
        db_calc.a = calc_update.a
        dirty = True

    if calc_update.b is not None:
        db_calc.b = calc_update.b
        dirty = True

    if calc_update.type is not None:
        # store lowercase string value in DB
        db_calc.type = calc_update.type.value
        dirty = True

    if calc_update.note is not None:
        db_calc.note = calc_update.note

    if dirty:
        # Determine CalculationType enum from stored string if needed
        current_type = (
            calc_update.type
            if calc_update.type is not None
            else schemas.CalculationType(db_calc.type)
        )
        result = CalculationFactory.calculate(db_calc.a, db_calc.b, current_type)
        db_calc.result = result

    db.commit()
    db.refresh(db_calc)
    return db_calc


def delete_calculation(db: Session, db_calc: models.Calculation) -> None:
    db.delete(db_calc)
    db.commit()
