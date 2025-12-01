import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine, SessionLocal

client = TestClient(app)


@pytest.fixture(autouse=True, scope="module")
def setup_db():
    # Fresh schema for this module's tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_user():
    payload = {
        "username": "m12_alice",
        "email": "m12_alice@example.com",
        "password": "secret123",
    }
    resp = client.post("/users/register", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data


def test_login_success():
    # user already created in previous test
    payload = {
        "identifier": "m12_alice",
        "password": "secret123",
    }
    resp = client.post("/users/login", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["message"] == "Login successful"
    assert data["user"]["username"] == "m12_alice"


def test_login_invalid_password():
    payload = {
        "identifier": "m12_alice",
        "password": "wrong-password",
    }
    resp = client.post("/users/login", json=payload)
    assert resp.status_code == 401
