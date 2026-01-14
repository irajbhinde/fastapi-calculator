import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Calculation
from app.schemas import CalculationCreate, CalculationType
from app.calculation_factory import CalculationFactory

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db",
)


@pytest.fixture(scope="module")
def db():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSession()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_insert_calculation_record(db):
    payload = CalculationCreate(a=2, b=3, type=CalculationType.ADD)
    result = CalculationFactory.compute(payload.a, payload.b, payload.type)

    calc = Calculation(
        a=payload.a,
        b=payload.b,
        type=payload.type.value,
        result=result,
        user_id=None,
    )

    db.add(calc)
    db.commit()
    db.refresh(calc)

    assert calc.id is not None
    assert calc.a == 2
    assert calc.b == 3
    assert calc.type == "add"
    assert calc.result == 5


def test_divide_by_zero_not_allowed_schema():
    with pytest.raises(Exception):
        CalculationCreate(a=1, b=0, type=CalculationType.DIVIDE)
