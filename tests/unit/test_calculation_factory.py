# tests/unit/test_calculation_factory.py
from pydantic import ValidationError
import pytest

from app.calculation_factory import CalculationFactory
from app.schemas import CalculationCreate, CalculationType


def test_factory_add():
    result = CalculationFactory.compute(2, 3, CalculationType.ADD)
    assert result == 5


def test_factory_subtract():
    result = CalculationFactory.compute(5, 3, CalculationType.SUBTRACT)
    assert result == 2


def test_factory_multiply():
    result = CalculationFactory.compute(4, 3, CalculationType.MULTIPLY)
    assert result == 12


def test_factory_divide():
    result = CalculationFactory.compute(10, 2, CalculationType.DIVIDE)
    assert result == 5


def test_factory_invalid_type():
    with pytest.raises(ValueError):
        # type: ignore[arg-type]  # simulate a bad type
        CalculationFactory.compute(1, 2, "unknown")  # not a valid operation


def test_calculation_create_disallows_divide_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(a=1, b=0, type=CalculationType.DIVIDE)
