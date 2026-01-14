import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.database import Base
from app import schemas, models, crud

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db"
)

@pytest.fixture(scope="module")
def db():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # make sure tables exist for tests
    Base.metadata.create_all(bind=engine)
    session = TestingSession()
    yield session
    session.rollback()
    session.close()

def test_create_user_and_uniqueness(db):
    # fresh usernames each run
    u1 = crud.create_user(db, schemas.UserCreate(username="u_test1", email="u1@example.com", password="abc12345"))
    db.commit()
    assert u1.id is not None

    with pytest.raises(IntegrityError):
        crud.create_user(db, schemas.UserCreate(username="u_test1", email="u2@example.com", password="abc12345"))
        db.commit()
