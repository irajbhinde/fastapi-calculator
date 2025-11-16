from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
import time
import os

from .operations import add, subtract, multiply, divide
from .logger import get_logger

# --- DB imports for secure user model ---
from .database import Base, engine, SessionLocal
from . import schemas, models, crud

logger = get_logger("fastapi-calculator")

app = FastAPI(title="FastAPI Calculator", version="1.0.0")

# Ensure tables exist (demo/dev convenience)
Base.metadata.create_all(bind=engine)

# Static & templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ---- Middleware: basic request timing ----
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        process_time = (time.time() - start_time) * 1000
        logger.info("%s %s -> %s in %.2fms",
                    request.method,
                    request.url.path,
                    getattr(response, "status_code", "ERR"),
                    process_time)

# ---- DB session dependency ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- Models for calculator endpoints ----
class Operands(BaseModel):
    a: float
    b: float

# ---- Routes ----
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
        return JSONResponse(status_code=500, content={"error": str(e)})

# ---- Calculator API ----
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

@app.post("/users", response_model=schemas.UserRead)
def create_user_api(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Friendly pre-check; DB uniqueness still enforced
    if crud.get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = crud.create_user(db, payload)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users", response_model=list[schemas.UserRead])
def list_users_api(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
