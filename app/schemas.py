# app/schemas.py

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, StringConstraints, model_validator


# =========================
# User Schemas
# =========================

class UserBase(BaseModel):
    email: EmailStr
    username: Annotated[str, StringConstraints(min_length=3)]


class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(min_length=8)]


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# M12-style login (for /users/login, used by integration tests)
class UserLogin(BaseModel):
    # "identifier" can be username OR email
    identifier: Annotated[str, StringConstraints(min_length=1)]
    password: Annotated[str, StringConstraints(min_length=1)]


# M13 JWT login (for /login, used by frontend)
class JwtLogin(BaseModel):
    email: EmailStr
    password: str


# Token returned by JWT endpoints
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================
# Calculation Schemas
# =========================

class CalculationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    POWER = "power"


class CalculationBase(BaseModel):
    a: float
    b: float
    type: CalculationType
    note: Optional[str] = None


class CalculationCreate(CalculationBase):
    user_id: Optional[int] = None

    @model_validator(mode="after")
    def disallow_divide_by_zero(self):
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Division by zero is not allowed.")
        return self


class CalculationUpdate(BaseModel):
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[CalculationType] = None
    note: Optional[str] = None


class CalculationRead(CalculationBase):
    id: int
    result: Optional[float] = None
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CalculationStats(BaseModel):
    total_calculations: int
    add_count: int
    subtract_count: int
    multiply_count: int
    divide_count: int
    power_count: int
    average_a: Optional[float]
    average_b: Optional[float]
    average_result: Optional[float]