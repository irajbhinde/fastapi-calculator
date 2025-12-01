# 🧮 FastAPI Calculator + 🐘 PostgreSQL + 🔐 Secure Users + 🧩 Calculation Model + 🔑 Auth + CRUD API (Modules 9--12)

This repository contains the full backend system developed across
Modules 9 → 12:

# 🚀 Features Overview (Modules 9--12)

## ✅ Calculator API

Basic math operations (add, subtract, multiply, divide) served through
FastAPI.

## ✅ PostgreSQL Integration

Database fully containerized using Docker Compose.

## ✅ Secure User System

-   **POST /users/register** --- Registration\
-   **POST /users/login** --- Login\
-   Password hashing using **Passlib**
-   Unique email + username\
-   Pydantic validation

## ✅ Calculation Model (Module 11)

-   SQLAlchemy model for saved calculations\
-   Stores: `a`, `b`, `type`, `result`, `user_id`, `timestamp`
-   Factory pattern used to compute results
-   Full test suite (schema, logic, DB integration)

## ✅ CRUD API (Module 12)

Calculation BREAD routes: - **POST /calculations** --- create\
- **GET /calculations** --- list\
- **GET /calculations/{id}** --- read\
- **PUT /calculations/{id}** --- update\
- **DELETE /calculations/{id}** --- delete

## 🔐 Optional Authentication

Module 12 allows login; future Module 13 can lock endpoints using JWT.

## 🧪 Testing

-   Unit tests\
-   Integration tests (requires Postgres)\
-   Playwright E2E tests\
-   GitHub Actions automated testing

## 🐳 Docker + Docker Hub

A prebuilt Docker image is automatically generated on every successful
CI run.

------------------------------------------------------------------------

# 📁 Project Structure

    fastapi-calculator/
    ├── app/
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── security.py
    │   ├── calculation_factory.py
    │   ├── crud.py
    │   ├── database.py
    │   ├── operations.py
    │   ├── logger.py
    │   └── DockerFile
    ├── tests/
    │   ├── unit/
    │   ├── integration/
    │   └── e2e/
    ├── sql/
    ├── logs/
    ├── docker-compose.yml
    ├── requirements.txt
    ├── README.md
    └── FastAPI_Postgres_Assignment.pdf

------------------------------------------------------------------------

# ⚙️ Run Locally (Without Docker)

``` bash
python -m venv .venv
.venv/Scripts/activate       # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger UI:\
👉 http://localhost:8000/docs

------------------------------------------------------------------------

# 🐳 Run With Docker Compose (Recommended)

``` bash
docker-compose up --build
```

Then visit:

-   **FastAPI:** http://localhost:8000\
-   **Swagger Docs:** http://localhost:8000/docs\
-   **pgAdmin:** http://localhost:5050

Postgres credentials come from `.env`.

------------------------------------------------------------------------

# 🔐 Module 12 --- User Auth Endpoints

## Register

**POST /users/register**

Request:

``` json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "mypassword"
}
```

Response:

``` json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2025-11-16T19:37:32.867729"
}
```

## Login

**POST /users/login**

Request:

``` json
{
  "email": "alice@example.com",
  "password": "mypassword"
}
```

Response:

``` json
{
  "message": "Login successful",
  "user_id": 1
}
```

------------------------------------------------------------------------

# 🧩 Module 12 --- Calculation CRUD API

  Action     Route
  ---------- -------------------------------
  ✔ Create   **POST /calculations**
  ✔ Browse   **GET /calculations**
  ✔ Read     **GET /calculations/{id}**
  ✔ Update   **PUT /calculations/{id}**
  ✔ Delete   **DELETE /calculations/{id}**

All responses validated by `CalculationRead`.

------------------------------------------------------------------------

# 🧪 Module 12 --- Test Suite

## 🟦 Unit Tests

-   Factory pattern\
-   Arithmetic logic\
-   Schema validation\
-   Password hashing

## 🟧 Integration Tests

-   User register + login\
-   Calculation create + fetch + update + delete\
-   Database integrity tests\
-   Validation error handling

Run all tests:

``` bash
pytest -q
```

------------------------------------------------------------------------

# 🔁 CI/CD Pipeline (GitHub Actions)

Workflow includes: - Spinning up PostgreSQL\
- Installing Python + Node + Playwright\
- Running **unit**, **integration**, and **E2E** tests\
- Building Docker image\
- Pushing to Docker Hub

Workflow file: `.github/workflows/ci.yml`

------------------------------------------------------------------------

# 🐋 Docker Hub Deployment

Your auto-built image is available here:

👉 https://hub.docker.com/r/rajbhinde/fastapi-calculator

Pull it:

``` bash
docker pull rajbhinde/fastapi-calculator:latest
```

------------------------------------------------------------------------

# 📸 Screenshots 

Saved in path Screenshots/M12_Screenshots

------------------------------------------------------------------------

# 🧠 Reflection

During this module, I learned how backend systems grow from basic endpoints into organized, validated, and secure application logic. Building the user registration and login flow showed me why password hashing, input validation, and error handling matter in real projects. I saw how Pydantic schemas keep data in the right format and stop bad input before it gets to the database. Working on the calculation model highlighted the importance of clear data modeling, and using the factory pattern made me realize how good design can make logic simpler and the system easier to expand.

Setting up integration tests and using GitHub Actions gave me hands-on experience with real CI/CD workflows. I worked with environment variables, dockerized PostgreSQL, Playwright browser testing, and automated Docker Hub deployment. There were some tough moments, especially with dependencies, environment problems, and workflow failures, but fixing those issues taught me how professional backend pipelines work. In the end, I built a backend system that is tested, secure, containerized, and always deployed, which made me feel more confident about creating scalable, production-ready services.


------------------------------------------------------------------------

# 🌐 Repository Links

🔗 Main Repo:\
https://github.com/irajbhinde/fastapi-calculator

🔗 Module 12 Branch:\
https://github.com/irajbhinde/fastapi-calculator/tree/module-12

🔗 Docker Hub:\
https://hub.docker.com/r/rajbhinde/fastapi-calculator
