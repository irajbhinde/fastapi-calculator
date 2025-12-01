from __future__ import annotations

import os
import time
from typing import List

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine
from .logger import get_logger
from .operations import add, subtract, multiply, divide

logger = get_logger("fastapi-calculator")

app = FastAPI(title="FastAPI Calculator", version="1.0.0")

# Create tables on startup (safe if they already exist)
Base.metadata.create_all(bind=engine)

# Static & templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# ---------------------------
# DB dependency
# ---------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# Simple logging middleware
# ---------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        process_time = (time.time() - start_time) * 1000
        logger.info(
            "%s %s -> %s in %.2fms",
            request.method,
            request.url.path,
            getattr(response, "status_code", "ERR"),
            process_time,
        )


# ---------------------------
# Calculator UI + basic endpoints
# ---------------------------

class Operands(schemas.BaseModel):
    a: float
    b: float


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-ping")
def db_ping():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "up"}
    except Exception as e:
        logger.exception("DB ping failed")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/add")
async def add_endpoint(data: Operands):
    try:
        result = add(data.a, data.b)
        logger.info("Add: %s + %s = %s", data.a, data.b, result)
        return {"result": result}
    except Exception as e:
        logger.exception("Add failed")
        return JSONResponse(status_code=400, content={"detail": str(e)})


@app.post("/subtract")
async def subtract_endpoint(data: Operands):
    try:
        result = subtract(data.a, data.b)
        logger.info("Subtract: %s - %s = %s", data.a, data.b, result)
        return {"result": result}
    except Exception as e:
        logger.exception("Subtract failed")
        return JSONResponse(status_code=400, content={"detail": str(e)})


@app.post("/multiply")
async def multiply_endpoint(data: Operands):
    try:
        result = multiply(data.a, data.b)
        logger.info("Multiply: %s * %s = %s", data.a, data.b, result)
        return {"result": result}
    except Exception as e:
        logger.exception("Multiply failed")
        return JSONResponse(status_code=400, content={"detail": str(e)})


@app.post("/divide")
async def divide_endpoint(data: Operands):
    try:
        result = divide(data.a, data.b)
        logger.info("Divide: %s / %s = %s", data.a, data.b, result)
        return {"result": result}
    except ZeroDivisionError as zde:
        logger.warning("Divide by zero: a=%s b=%s", data.a, data.b)
        return JSONResponse(status_code=400, content={"detail": str(zde)})
    except Exception as e:
        logger.exception("Divide failed")
        return JSONResponse(status_code=400, content={"detail": str(e)})


# ---------------------------
# User API (existing + new auth)
# ---------------------------

@app.post(
    "/users",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user_api(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("Creating user via /users")
    user = crud.create_user(db, payload)
    return user


@app.get(
    "/users",
    response_model=list[schemas.UserRead],
)
def list_users_api(db: Session = Depends(get_db)):
    users = crud.list_users(db)
    return list(users)


@app.post(
    "/users/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Could check for existing username/email and return 400
    existing_username = crud.get_user_by_username(db, payload.username)
    existing_email = crud.get_user_by_email(db, payload.email)
    if existing_username or existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already in use",
        )
    user = crud.create_user(db, payload)
    return user


@app.post("/users/login")
def login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.verify_user_credentials(db, payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
        )
    return {
        "message": "Login successful",
        "user": schemas.UserRead.model_validate(user),
    }


# ---------------------------
# Calculation BREAD endpoints
# ---------------------------

@app.post(
    "/calculations",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_calculation_api(
    payload: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    calc = crud.create_calculation(db, payload)
    return calc


@app.get(
    "/calculations",
    response_model=list[schemas.CalculationRead],
)
def list_calculations_api(db: Session = Depends(get_db)):
    calcs = crud.list_calculations(db)
    return list(calcs)


@app.get(
    "/calculations/{calc_id}",
    response_model=schemas.CalculationRead,
)
def read_calculation_api(calc_id: int, db: Session = Depends(get_db)):
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return calc


@app.put(
    "/calculations/{calc_id}",
    response_model=schemas.CalculationRead,
)
def update_calculation_api(
    calc_id: int,
    payload: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if not any([payload.a is not None, payload.b is not None, payload.type is not None, payload.note is not None]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided",
        )
    calc = crud.update_calculation(db, calc, payload)
    return calc


@app.delete("/calculations/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation_api(calc_id: int, db: Session = Depends(get_db)):
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    crud.delete_calculation(db, calc)
    return None
