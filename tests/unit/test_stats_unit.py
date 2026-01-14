# tests/test_stats_unit.py
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.database import Base, engine, SessionLocal


def setup_module(module):
    # ensure fresh schema for this test module (depending on your test setup)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _make_session() -> Session:
    return SessionLocal()


def test_get_calculation_stats_counts_and_averages():
    db = _make_session()
    try:
        # seed some data
        db.add_all(
            [
                models.Calculation(a=1, b=2, type="add", result=3),
                models.Calculation(a=5, b=3, type="subtract", result=2),
                models.Calculation(a=2, b=4, type="multiply", result=8),
            ]
        )
        db.commit()

        stats: schemas.CalculationStats = crud.get_calculation_stats(db)

        assert stats.total_calculations == 3
        assert stats.add_count == 1
        assert stats.subtract_count == 1
        assert stats.multiply_count == 1
        assert stats.divide_count == 0
        assert stats.average_a is not None
        assert stats.average_b is not None
        assert stats.average_result is not None
    finally:
        db.close()
