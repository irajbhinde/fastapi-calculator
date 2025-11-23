# 🧮 FastAPI Calculator + 🐘 PostgreSQL + 🔐 Secure Users + 🧩 Calculation Model (Module 11)

This repository contains a full FastAPI application enhanced across multiple modules:
- **Module 9:** SQL operations with PostgreSQL + pgAdmin  
- **Module 10:** Secure user model with hashing + CI/CD  
- **Module 11:** Calculation model (SQLAlchemy), Pydantic validation, factory pattern, and full test coverage  

It includes:
- A calculator API  
- A secure `User` model  
- A robust `Calculation` model + factory  
- Full test suite (unit, integration, e2e)  
- CI pipeline with PostgreSQL + Playwright  
- Docker image deployment to Docker Hub  

---

## 🚀 Features Overview

### ✅ Calculator API (Module 8)
Endpoints:
- `POST /add`
- `POST /subtract`
- `POST /multiply`
- `POST /divide`
- `GET /health`

---

## 🔐 Secure User Model (Module 10)

### SQLAlchemy `User` model:
- `id`, `username`, `email`, `password_hash`, `created_at`
- Unique constraints on username & email
- Password hashing via Passlib

### Pydantic Schemas:
- **UserCreate** → validates username, email, password
- **UserRead** → safe response (no password hash)

### Endpoints:
- `POST /users` → create user
- `GET /users` → list users

---

## 🧩 Calculation Model (Module 11)

### SQLAlchemy `Calculation` model:
Fields:
- `a: float`
- `b: float`
- `type: Enum(add, sub, mul, div)`
- `result: float`
- `created_at`
- `user_id` (optional FK)

### Pydantic Schemas:
- **CalculationType** (Enum)
- **CalculationCreate**
- **CalculationRead**

### Validation:
- No division by zero  
- Only valid operation types allowed  

### Factory Pattern:
`CalculationFactory` determines which operation to use and computes the result.

Example:
```py
calc = CalculationFactory.create(a=2, b=3, calc_type="add")
assert calc.compute() == 5
```

---

## 🧪 Tests

### Unit Tests:
- Calculation factory  
- Schemas validation  
- Security hashing  
- Arithmetic operations  

### Integration Tests:
- User model (unique email, hashed password)  
- Calculation model insert + DB behavior  
- FastAPI API endpoints  

### End-to-End Tests:
- Playwright tests for calculator UI  

---

## 🐳 Docker & Docker Compose

### Run Whole Stack:
```bash
docker-compose up --build
```

Services:
- FastAPI → http://localhost:8000  
- pgAdmin → http://localhost:5050  

---

## 🐋 Docker Hub Image

Pull it:
```bash
docker pull rajbhinde/fastapi-calculator:latest
```

Docker Hub:  
https://hub.docker.com/r/rajbhinde/fastapi-calculator

---

## ⚙️ Local Development

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🧠 CI/CD Pipeline

The GitHub Actions workflow:

✔ Spins up PostgreSQL  
✔ Installs Python + Node + Playwright  
✔ Runs unit + integration + e2e tests  
✔ Builds Docker image  
✔ Pushes to Docker Hub using repo secrets  

Workflow file: `.github/workflows/ci.yml`

---

## 📁 Project Structure

```
fastapi-calculator/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── calculation_factory.py
│   ├── database.py
│   ├── operations.py
│   ├── logger.py
│   └── DockerFile
├── sql/
│   └── steps.sql
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── logs/
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

## 📄 Module 11 Screenshots

Added in the Screenshots folder

---
