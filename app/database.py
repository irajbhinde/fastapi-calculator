# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# -----------------------------
# DATABASE CONFIG
# -----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# -----------------------------
# SQLAlchemy Base (single source)
# -----------------------------
class Base(DeclarativeBase):
    """Shared Declarative Base for all models."""
    pass


# -----------------------------
# Dependency: get_db()
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Initialize DB tables on startup
# -----------------------------
def init_db():
    # Import models so SQLAlchemy knows them
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

init_db()
