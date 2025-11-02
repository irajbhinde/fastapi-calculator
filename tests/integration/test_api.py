
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_add_endpoint():
    r = client.post("/add", json={"a": 2, "b": 3})
    assert r.status_code == 200
    assert r.json()["result"] == 5

def test_subtract_endpoint():
    r = client.post("/subtract", json={"a": 5, "b": 2})
    assert r.status_code == 200
    assert r.json()["result"] == 3

def test_multiply_endpoint():
    r = client.post("/multiply", json={"a": 3, "b": 4})
    assert r.status_code == 200
    assert r.json()["result"] == 12

def test_divide_endpoint():
    r = client.post("/divide", json={"a": 8, "b": 4})
    assert r.status_code == 200
    assert r.json()["result"] == 2

def test_divide_by_zero_endpoint():
    r = client.post("/divide", json={"a": 1, "b": 0})
    assert r.status_code == 400
    assert "Division by zero" in r.json()["detail"]
