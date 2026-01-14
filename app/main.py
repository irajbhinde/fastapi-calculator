# app/main.py
from __future__ import annotations

import time
from pathlib import Path
from typing import List
from fastapi.routing import APIRoute


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
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import engine, get_db, init_db
from .logger import get_logger
from .operations import add, subtract, multiply, divide
from . import crud, models, schemas, security
from .operations import power

logger = get_logger("fastapi-calculator")

app = FastAPI(title="FastAPI Calculator", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent

# Templates & static
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


# ---------------------------
# Startup: init DB
# ---------------------------

@app.on_event("startup")
def on_startup():
    init_db()


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

class Operands(BaseModel):
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


@app.post("/power")
async def power_endpoint(data: Operands):
    try:
        result = power(data.a, data.b)
        logger.info("Power: %s ** %s = %s", data.a, data.b, result)
        return {"result": result}
    except Exception as e:
        logger.exception("Power failed")
        return JSONResponse(status_code=400, content={"detail": str(e)})


# ---------------------------
# User API (existing + legacy auth for tests)
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
    response_model=List[schemas.UserRead],
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
def legacy_login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    M12-style login: accepts 'identifier' (username or email) + password.
    Used by integration tests.
    """
    user = crud.verify_user_credentials(db, payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
        )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat()
            if getattr(user, "created_at", None)
            else None,
        },
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
    response_model=List[schemas.CalculationRead],
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
    if not any(
        [
            payload.a is not None,
            payload.b is not None,
            payload.type is not None,
            payload.note is not None,
        ]
    ):
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


# ---------------------------
# Front-end pages for auth (HTML)
# ---------------------------

REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Register</title>
    <link rel="stylesheet" href="/static/styles.css" />
  </head>
  <body>
    <div class="auth-container">
      <h1>Register</h1>

      <form id="register-form" novalidate>
        <label>
          Username
          <input type="text" id="reg-username" required />
        </label>
        <label>
          Email
          <input type="email" id="reg-email" required />
        </label>
        <label>
          Password
          <input type="password" id="reg-password" required />
        </label>
        <label>
          Confirm Password
          <input type="password" id="reg-confirm" required />
        </label>
        <button type="submit">Register</button>
      </form>

      <p id="register-error" style="color: red;"></p>
      <p id="register-success" style="color: green;"></p>

      <p><a href="/login">Already have an account? Log in</a></p>

      <script src="/static/auth.js"></script>
    </div>
  </body>
</html>
"""


LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Login</title>
    <link rel="stylesheet" href="/static/styles.css" />
  </head>
  <body>
    <div class="auth-container">
      <h1>Login</h1>

      <form id="login-form" novalidate>
        <label>
          Email
          <input type="email" id="login-identifier" required />
        </label>
        <label>
          Password
          <input type="password" id="login-password" required />
        </label>
        <button type="submit">Login</button>
      </form>

      <p id="login-error" style="color: red;"></p>
      <p id="login-success" style="color: green;"></p>

      <p><a href="/register">Need an account? Register</a></p>

      <script src="/static/auth.js"></script>
    </div>
  </body>
</html>
"""


@app.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def register_page():
    # This log line is just to prove the handler runs
    print(">>> /register handler EXECUTED")

    html = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Register</title>
        <link rel="stylesheet" href="/static/styles.css" />
      </head>
      <body>
        <div class="auth-container">
          <h1>Register</h1>

          <form id="register-form" novalidate>
            <label>
              Username
              <input type="text" id="reg-username" required />
            </label>
            <label>
              Email
              <input type="email" id="reg-email" required />
            </label>
            <label>
              Password
              <input type="password" id="reg-password" required />
            </label>
            <label>
              Confirm Password
              <input type="password" id="reg-confirm" required />
            </label>
            <button type="submit">Register</button>
          </form>

          <p id="register-error" style="color: red;"></p>
          <p id="register-success" style="color: green;"></p>

          <p><a href="/login">Already have an account? Log in</a></p>

          <script src="/static/auth.js"></script>
        </div>
      </body>
    </html>
    """

    return HTMLResponse(content=html, status_code=200)


@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_page():
    # IMPORTANT: return the HTML string directly
    return LOGIN_HTML


# ---------------------------
# JWT API endpoints (Module 13)
# ---------------------------

@app.post(
    "/register",
    response_model=schemas.Token,
    status_code=status.HTTP_201_CREATED,
)
def register_jwt(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    M13 JWT register:

    - If user (by username or email) already exists, reuse that user
      and return a token (idempotent).
    - Otherwise, create a new user and return a token.
    """

    # Try to find existing user by username or email
    user = crud.get_user_by_username(db, payload.username)
    if not user:
        user = crud.get_user_by_email(db, payload.email)

    # If no user yet, create one
    if not user:
        user = crud.create_user(db, payload)

    # Always issue a token
    token = security.create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=schemas.Token)
def login_jwt(payload: schemas.JwtLogin, db: Session = Depends(get_db)):
    """
    M13 JWT login: used by the frontend (auth.js).
    Accepts:
      {
        "email": "...",
        "password": "..."
      }
    Returns:
      {
        "access_token": "...",
        "token_type": "bearer"
      }
    """

    logger.info(f"/login attempt email={payload.email}")

    # 1. Look up user by email
    user = crud.get_user_by_email(db, payload.email)

    if not user:
        logger.warning(f"/login: no user found for email={payload.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
        )

    # 2. Verify password using the same hashing as everywhere else
    if not security.verify_password(payload.password, user.password_hash):
        logger.warning(f"/login: bad password for user_id={user.id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
        )

    # 3. Issue JWT
    token = security.create_access_token(subject=user.id)
    logger.info(f"/login: success for user_id={user.id}")
    return {"access_token": token, "token_type": "bearer"}




@app.get("/debug-routes", include_in_schema=False)
def debug_routes():
    routes_info = []
    for r in app.routes:
        if isinstance(r, APIRoute):
            routes_info.append(
                {
                    "path": r.path,
                    "name": r.name,
                    "methods": sorted(list(r.methods or [])),
                }
            )
    return routes_info

@app.get("/calculations-ui", response_class=HTMLResponse)
async def calculations_ui(request: Request):
    """
    Front-end page for full BREAD operations on calculations.
    Uses /calculations API under the hood.
    """
    return templates.TemplateResponse("calculations.html", {"request": request})

@app.get("/api/calculations/stats", response_model=schemas.CalculationStats)
def get_calculations_stats(db: Session = Depends(get_db)):
    """
    Return global usage stats for all calculations in the system.
    """
    return crud.get_calculation_stats(db)
