
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import time

from .operations import add, subtract, multiply, divide
from .logger import get_logger

logger = get_logger("fastapi-calculator")

app = FastAPI(title="FastAPI Calculator", version="1.0.0")

# Static & templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Simple request logging middleware
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

class Operands(BaseModel):
    a: float
    b: float

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok"}

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
