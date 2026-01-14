# tests/integration/test_stats_route.py
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app import models

client = TestClient(app)


def test_stats_route_returns_shape_and_values():
    # Ensure tables exist for this test DB
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Clear any existing data
        db.query(models.Calculation).delete()
        db.commit()

        # Seed one calculation
        db.add(models.Calculation(a=2, b=3, type="add", result=5))
        db.commit()
    finally:
        db.close()

    resp = client.get("/api/calculations/stats")
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_calculations"] >= 1
    assert "add_count" in data
    assert "average_a" in data
