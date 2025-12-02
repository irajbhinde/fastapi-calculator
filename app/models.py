# app/models.py
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# -----------------------------
# USER MODEL
# -----------------------------
class User(Base):
    __tablename__ = "users_secure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )

    calculations: Mapped[List["Calculation"]] = relationship(
        "Calculation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# -----------------------------
# CALCULATION MODEL
# -----------------------------
class Calculation(Base):
    """
    Stores a single calculator operation.

    - `type` is a string like "add", "subtract", "multiply", "divide"
    - `result` is stored
    - `user_id` optionally links to users_secure.id
    """

    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    a: Mapped[float] = mapped_column(Float, nullable=False)
    b: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    result: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Optional note column
    note: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # 👇 make sure SQLAlchemy clearly sees this as a ForeignKey
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users_secure.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="calculations",
    )
