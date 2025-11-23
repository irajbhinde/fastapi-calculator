# app/models.py
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users_secure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
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


class Calculation(Base):
    """
    Stores a single calculator operation.

    - `type` is a string like "add", "subtract", "multiply", "divide"
    - `result` can be stored or computed on demand; here we choose to store it
    - `user_id` is optional, but if set it references users_secure.id
    """

    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    a: Mapped[float] = mapped_column(Float, nullable=False)
    b: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    result: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users_secure.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[Optional[User]] = relationship(
        "User",
        back_populates="calculations",
    )
