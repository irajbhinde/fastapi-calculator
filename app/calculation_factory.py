# app/calculation_factory.py
from __future__ import annotations

from typing import Callable, Union

from .operations import add, subtract, multiply, divide
from .schemas import CalculationType


OperationInput = Union[str, CalculationType]


class CalculationFactory:
    """
    Factory for picking the correct calculation function based on type.
    """

    @staticmethod
    def create(operation_type: OperationInput) -> Callable[[float, float], float]:
        # Normalize input (string or enum) to lowercase string key
        if isinstance(operation_type, CalculationType):
            key = operation_type.value
        else:
            key = str(operation_type).lower().strip()

        if key == "add":
            return add
        elif key in ("sub", "subtract"):
            return subtract
        elif key in ("mul", "multiply"):
            return multiply
        elif key in ("div", "divide"):
            return divide
        else:
            raise ValueError(f"Unknown calculation type: {operation_type}")

    @classmethod
    def compute(cls, a: float, b: float, operation_type: OperationInput) -> float:
        """
        Convenience helper used by tests:
        CalculationFactory.compute(2, 3, CalculationType.ADD) -> 5
        """
        func = cls.create(operation_type)
        return func(a, b)

    @staticmethod
    def calculate(a: float, b: float, operation_type: OperationInput) -> float:
        """
        Alias expected by CRUD and some tests.
        """
        return CalculationFactory.compute(a, b, operation_type)
