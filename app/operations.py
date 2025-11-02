
from typing import Union

Number = Union[int, float]

def _coerce(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        raise ValueError("Inputs must be numbers or numeric strings")

def add(a: Number, b: Number) -> float:
    return _coerce(a) + _coerce(b)

def subtract(a: Number, b: Number) -> float:
    return _coerce(a) - _coerce(b)

def multiply(a: Number, b: Number) -> float:
    return _coerce(a) * _coerce(b)

def divide(a: Number, b: Number) -> float:
    b_val = _coerce(b)
    if b_val == 0:
        raise ZeroDivisionError("Division by zero")
    return _coerce(a) / b_val
