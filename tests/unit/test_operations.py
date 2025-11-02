
import math
import pytest
from app.operations import add, subtract, multiply, divide

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (1.5, 2.5, 4.0),
    ("3", "4", 7.0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("a,b,expected", [
    (5, 2, 3),
    (2.5, 1.5, 1.0),
    ("5", "3", 2.0),
    (-1, -1, 0),
])
def test_subtract(a, b, expected):
    assert subtract(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("a,b,expected", [
    (3, 4, 12),
    (2.5, 2, 5.0),
    ("3", "2", 6.0),
    (-1, 2, -2),
])
def test_multiply(a, b, expected):
    assert multiply(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("a,b,expected", [
    (8, 4, 2),
    (5, 2, 2.5),
    ("9", "3", 3.0),
    (-6, 2, -3),
])
def test_divide(a, b, expected):
    assert divide(a, b) == pytest.approx(expected)

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

@pytest.mark.parametrize("func", [add, subtract, multiply, divide])
def test_invalid_input(func):
    with pytest.raises(ValueError):
        func("abc", 1)
