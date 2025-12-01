from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


# ---------- User Schemas (keep your existing ones) ----------

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    identifier: str = Field(
        ...,
        description="Username or email",
        min_length=3,
    )
    password: str = Field(min_length=6, max_length=128)


# ---------- Calculation Schemas ----------

class CalculationType(str, Enum):
    # UPPERCASE names so tests can use CalculationType.ADD etc.
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType
    user_id: Optional[int] = None
    note: Optional[str] = None

    @model_validator(mode="after")
    def validate_division(self) -> "CalculationCreate":
        # Prevent divide-by-zero cases
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Divisor 'b' cannot be zero for divide operations")
        return self


class CalculationUpdate(BaseModel):
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[CalculationType] = None
    note: Optional[str] = None

    # For this assignment we don't strictly need extra validation here;
    # tests care about create() divide-by-zero, not update().
    @model_validator(mode="after")
    def validate_division(self) -> "CalculationUpdate":
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Divisor 'b' cannot be zero for divide operations")
        return self


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: Optional[float]
    user_id: Optional[int] = None
    note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
