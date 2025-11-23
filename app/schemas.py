# app/schemas.py
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, model_validator


# ---------- User Schemas ----------

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------- Calculation Schemas ----------

class CalculationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType
    user_id: int | None = None

    @model_validator(mode="after")
    def validate_division(self) -> "CalculationCreate":
        # Prevent divide-by-zero cases
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Divisor 'b' cannot be zero for divide operations")
        return self


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: float | None
    user_id: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
