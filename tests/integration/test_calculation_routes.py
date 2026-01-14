import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine

client = TestClient(app)


@pytest.fixture(autouse=True, scope="module")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_calculation():
    payload = {"a": 2, "b": 3, "type": "add"}
    resp = client.post("/calculations", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["a"] == 2
    assert data["b"] == 3
    assert data["type"] == "add"
    assert data["result"] == 5


def test_list_calculations():
    resp = client.get("/calculations")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read_update_delete_calculation():
    # create one
    payload = {"a": 10, "b": 5, "type": "subtract"}
    create_resp = client.post("/calculations", json=payload)
    assert create_resp.status_code == 201
    calc_id = create_resp.json()["id"]

    # read
    resp = client.get(f"/calculations/{calc_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == calc_id
    assert data["result"] == 5

    # update
    update_payload = {"a": 20, "b": 5, "type": "divide"}
    update_resp = client.put(f"/calculations/{calc_id}", json=update_payload)
    assert update_resp.status_code == 200, update_resp.text
    updated = update_resp.json()
    assert updated["result"] == 4

    # delete
    delete_resp = client.delete(f"/calculations/{calc_id}")
    assert delete_resp.status_code == 204

    # ensure gone
    get_again = client.get(f"/calculations/{calc_id}")
    assert get_again.status_code == 404


def test_divide_by_zero_validation():
    payload = {"a": 1, "b": 0, "type": "divide"}
    resp = client.post("/calculations", json=payload)
    # Pydantic validator should fail -> 422
    assert resp.status_code == 422
