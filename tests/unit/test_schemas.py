import pytest
from pydantic import ValidationError
from app.schemas import UserCreate

def test_usercreate_valid():
    u = UserCreate(username="alice", email="alice@example.com", password="secret12")
    assert u.username == "alice"

def test_usercreate_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="bob", email="not-an-email", password="secret12")

def test_usercreate_short_password():
    with pytest.raises(ValidationError):
        UserCreate(username="bob", email="bob@example.com", password="123")
