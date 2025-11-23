# app/calculation_factory.py
from abc import ABC, abstractmethod

from .operations import add, subtract, multiply, divide
from .schemas import CalculationType


class CalculationStrategy(ABC):
    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        ...


class AddStrategy(CalculationStrategy):
    def compute(self, a: float, b: float) -> float:
        return add(a, b)


class SubtractStrategy(CalculationStrategy):
    def compute(self, a: float, b: float) -> float:
        return subtract(a, b)


class MultiplyStrategy(CalculationStrategy):
    def compute(self, a: float, b: float) -> float:
        return multiply(a, b)


class DivideStrategy(CalculationStrategy):
    def compute(self, a: float, b: float) -> float:
        # We rely on Pydantic to prevent b == 0, and operations.divide for logic.
        return divide(a, b)


class CalculationFactory:
    """
    Factory for picking the correct calculation strategy based on type.
    """

    _strategies: dict[CalculationType, CalculationStrategy] = {
        CalculationType.ADD: AddStrategy(),
        CalculationType.SUBTRACT: SubtractStrategy(),
        CalculationType.MULTIPLY: MultiplyStrategy(),
        CalculationType.DIVIDE: DivideStrategy(),
    }

    @classmethod
    def get_strategy(cls, calc_type: CalculationType) -> CalculationStrategy:
        try:
            return cls._strategies[calc_type]
        except KeyError:
            raise ValueError(f"Unsupported calculation type: {calc_type}")

    @classmethod
    def compute(cls, a: float, b: float, calc_type: CalculationType) -> float:
        strategy = cls.get_strategy(calc_type)
        return strategy.compute(a, b)
